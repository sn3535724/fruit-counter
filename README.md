# Подсчёт фруктов в магазине/на конвейере

Веб-приложение для детекции и подсчёта яблок, бананов и апельсинов на
изображении. Для распознавания используется предобученная YOLOv8n без
дополнительного обучения.

## Запуск

Требуется Python 3.11.

```bash
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска откройте в браузере `http://localhost:8000`.
Веса модели `yolov8n.pt` загрузятся автоматически при первом запуске и не
хранятся в Git.

Приложение принимает изображения через `POST /process`, сохраняет результаты
в SQLite и показывает историю через `GET /history`. Историю можно скачать
через `/export/pdf` и `/export/excel`.

## Структура

- `app/` — backend на FastAPI и модули обработки данных;
- `static/` — HTML, CSS, JavaScript и результаты обработки;
- `tests/` — тесты приложения.
