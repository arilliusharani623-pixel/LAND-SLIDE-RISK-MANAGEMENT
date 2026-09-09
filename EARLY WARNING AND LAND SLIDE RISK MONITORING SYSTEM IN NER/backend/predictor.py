from collections.abc import Mapping
from typing import Any

import pandas as pd


class PredictionError(ValueError):
    pass


_ALIASES: dict[str, tuple[str, ...]] = {
    "rainfall": ("rainfall", "rainfall_mm", "annual_rainfall", "avg_annual_rainfall"),
    "slope": ("slope", "slope_angle", "slope_angle_degrees"),
    "soil_moisture": ("soil_moisture", "soil_saturation", "soil_saturation_percent"),
    "elevation": ("elevation", "elevation_m", "elevation_meters"),
}


def _value_for_feature(feature: str, values: Mapping[str, float], index: int) -> float:
    normalized = feature.strip().lower().replace(" ", "_")
    for source_name, aliases in _ALIASES.items():
        if normalized in aliases:
            return float(values[source_name])
    # The notebook's landslide dataset contains binary soil/land-cover columns.
    if "soil_type" in normalized or normalized in {"vegetation_density", "land_cover"}:
        return 0.0
    # Preserve a deterministic input shape for models without feature_names_in_.
    fallback = (values["rainfall"], values["slope"], values["soil_moisture"], values["elevation"])
    return fallback[index % len(fallback)]


def build_features(model: Any, values: Mapping[str, float]) -> pd.DataFrame:
    names = getattr(model, "feature_names_in_", None)
    if names is None:
        count = int(getattr(model, "n_features_in_", 4))
        names = [f"feature_{index + 1}" for index in range(count)]
    features = [_value_for_feature(str(name), values, index) for index, name in enumerate(names)]
    return pd.DataFrame([features], columns=[str(name) for name in names])


def predict_risk(model: Any, values: Mapping[str, float]) -> tuple[int, str]:
    frame = build_features(model, values)
    try:
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(frame)[0]
            classes = list(getattr(model, "classes_", range(len(probabilities))))
            positive_index = classes.index(1) if 1 in classes else len(probabilities) - 1
            probability = float(probabilities[positive_index])
        else:
            probability = float(model.predict(frame)[0])
    except Exception as exc:
        raise PredictionError(f"Model prediction failed: {exc}") from exc
    score = max(0, min(100, round(probability * 100)))
    level = "High" if score >= 80 else "Medium" if score >= 50 else "Low"
    return score, level
