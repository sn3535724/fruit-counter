from app import db


def test_save_request_persists(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "history.db")
    db.init_db()
    db.save_request(
        {"apple": 1, "banana": 2, "orange": 3, "total": 6},
        "/static/results/example.jpg",
    )

    history = db.get_history()
    assert len(history) == 1
    assert history[0]["orange"] == 3
    assert history[0]["total"] == 6
