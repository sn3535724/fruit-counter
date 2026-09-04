import numpy as np

from app.inference import detect


def test_detect_on_smoke_image() -> None:
    image = np.zeros((128, 128, 3), dtype=np.uint8)
    annotated, counts = detect(image)

    assert annotated.shape == image.shape
    assert set(counts) == {"apple", "banana", "orange", "total"}
    assert counts["total"] >= 0
