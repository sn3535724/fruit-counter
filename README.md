# Fruit Counter

Учебное веб-приложение для детекции и подсчёта фруктов на изображении.
Приложение использует предобученную модель YOLOv8n и учитывает яблоки,
бананы и апельсины.

## Запуск

Требуется Python 3.11.

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

После запуска откройте в браузере `http://localhost:8000`.
Веса модели `yolov8n.pt` загрузятся автоматически при первом запуске и не
хранятся в Git.

## Структура

- `app/` — backend на FastAPI и модули обработки данных;
- `static/` — HTML, CSS, JavaScript и результаты обработки;
- `tests/` — smoke-тесты;
- `ForCodex.md` — инструкции по этапам разработки.
