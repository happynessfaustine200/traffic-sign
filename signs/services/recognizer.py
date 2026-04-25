from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image

from signs.models import TrafficSignClass, TrainingImage


@dataclass
class PredictionResult:
    sign_class: TrafficSignClass | None
    confidence: float


def extract_features(image_field) -> list[float]:
    image = Image.open(image_field).convert("RGB")
    image = image.resize((32, 32))
    image_array = np.asarray(image, dtype=np.float32) / 255.0

    histogram = []
    for channel in range(3):
        hist, _ = np.histogram(image_array[:, :, channel], bins=16, range=(0, 1), density=True)
        histogram.extend(hist.tolist())

    # Keep the vector compact while retaining coarse color + shape signal.
    downsampled = image_array[::4, ::4, :].flatten().tolist()
    return histogram + downsampled


def predict_sign(image_field) -> PredictionResult:
    training_samples = list(
        TrainingImage.objects.select_related("sign_class").exclude(feature_vector=[])
    )
    if not training_samples:
        return PredictionResult(sign_class=None, confidence=0.0)

    query_features = np.array(extract_features(image_field), dtype=np.float32)

    best_sample = None
    best_distance = float("inf")

    for sample in training_samples:
        sample_features = np.array(sample.feature_vector, dtype=np.float32)
        if sample_features.size != query_features.size:
            continue

        distance = float(np.linalg.norm(query_features - sample_features))
        if distance < best_distance:
            best_distance = distance
            best_sample = sample

    if best_sample is None:
        return PredictionResult(sign_class=None, confidence=0.0)

    confidence = 1.0 / (1.0 + best_distance)
    return PredictionResult(sign_class=best_sample.sign_class, confidence=confidence)
