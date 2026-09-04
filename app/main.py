from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .db import get_history, init_db, save_request
from .inference import detect
from .reports import export_excel, export_pdf


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
RESULTS_DIR = STATIC_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Подсчёт фруктов в магазине/на конвейере")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/process")
async def process_image(file: UploadFile = File(...)) -> dict[str, object]:
    contents = await file.read()
    image = cv2.imdecode(np.frombuffer(contents, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Не удалось прочитать изображение")

    annotated, counts = detect(image)
    filename = f"{uuid4()}.jpg"
    result_path = RESULTS_DIR / filename
    if not cv2.imwrite(str(result_path), annotated):
        raise HTTPException(status_code=500, detail="Не удалось сохранить результат")

    image_url = f"/static/results/{filename}"
    save_request(counts, image_url)
    return {"image_url": image_url, "counts": counts}


@app.get("/history")
def history() -> list[dict[str, object]]:
    return get_history()


@app.get("/export/pdf")
def export_pdf_report() -> StreamingResponse:
    report = export_pdf(get_history())
    return StreamingResponse(
        report,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=fruit-history.pdf"},
    )


@app.get("/export/excel")
def export_excel_report() -> StreamingResponse:
    report = export_excel(get_history())
    return StreamingResponse(
        report,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=fruit-history.xlsx"},
    )
