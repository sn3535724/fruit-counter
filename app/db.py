from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DB_PATH = Path(__file__).resolve().parent.parent / "history.db"
MOSCOW_TIME_FORMAT = "%d.%m.%Y %H:%M"

try:
    MOSCOW_TZ = ZoneInfo("Europe/Moscow")
except ZoneInfoNotFoundError:
    MOSCOW_TZ = timezone(timedelta(hours=3))


@contextmanager
def _connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    with _connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                apple INTEGER NOT NULL,
                banana INTEGER NOT NULL,
                orange INTEGER NOT NULL,
                total INTEGER NOT NULL,
                image_path TEXT NOT NULL
            )
            """
        )
        _format_legacy_timestamps(connection)


def _format_legacy_timestamps(connection: sqlite3.Connection) -> None:
    rows = connection.execute("SELECT id, timestamp FROM requests").fetchall()
    for row in rows:
        try:
            timestamp = datetime.fromisoformat(row["timestamp"])
        except ValueError:
            continue

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        formatted = timestamp.astimezone(MOSCOW_TZ).strftime(MOSCOW_TIME_FORMAT)
        connection.execute(
            "UPDATE requests SET timestamp = ? WHERE id = ?",
            (formatted, row["id"]),
        )


def save_request(counts: dict[str, int], image_path: str) -> None:
    timestamp = datetime.now(MOSCOW_TZ).strftime(MOSCOW_TIME_FORMAT)
    with _connection() as connection:
        connection.execute(
            """
            INSERT INTO requests (timestamp, apple, banana, orange, total, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                counts["apple"],
                counts["banana"],
                counts["orange"],
                counts["total"],
                image_path,
            ),
        )


def get_history() -> list[dict[str, Any]]:
    with _connection() as connection:
        rows = connection.execute(
            """
            SELECT id, timestamp, apple, banana, orange, total, image_path
            FROM requests
            ORDER BY id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]
