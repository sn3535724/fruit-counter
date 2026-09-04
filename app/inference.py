from __future__ import annotations

import cv2
import numpy as np
from ultralytics import YOLO


TARGET_CLASSES = {"apple", "banana", "orange"}
CONFIDENCE_THRESHOLD = 0.15
IMAGE_SIZE = 1280
model = YOLO("yolov8n.pt")


def detect(image: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Detect target fruits and return an annotated image with their counts."""
    counts = {"apple": 0, "banana": 0, "orange": 0, "total": 0}
    annotated = image.copy()
    result = model.predict(
        source=image,
        conf=CONFIDENCE_THRESHOLD,
        imgsz=IMAGE_SIZE,
        verbose=False,
    )[0]
    names = result.names

    for box in result.boxes:
        class_id = int(box.cls[0].item())
        class_name = names.get(class_id) if isinstance(names, dict) else names[class_id]
        if class_name not in TARGET_CLASSES:
            continue

        confidence = float(box.conf[0].item())
        x1, y1, x2, y2 = (int(value) for value in box.xyxy[0].tolist())
        color = (0, 180, 0)
        label = f"{class_name} {confidence:.2f}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            annotated,
            label,
            (x1, max(y1 - 8, 18)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )
        counts[class_name] += 1
        counts["total"] += 1

    return annotated, counts
