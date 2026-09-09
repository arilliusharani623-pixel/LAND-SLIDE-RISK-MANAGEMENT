import logging
from pathlib import Path
from typing import Any

import joblib

logger = logging.getLogger(__name__)


class ModelLoadError(RuntimeError):
    pass


def load_model(model_path: Path) -> Any:
    if not model_path.exists():
        raise ModelLoadError(
            f"Model artifact not found at {model_path}. Run scripts/export_model.py after executing the notebook."
        )
    if not model_path.is_file():
        raise ModelLoadError(f"Model path is not a file: {model_path}")
    try:
        model = joblib.load(model_path)
    except Exception as exc:
        logger.exception("Unable to load model artifact")
        raise ModelLoadError(f"Unable to load model artifact: {exc}") from exc
    if not hasattr(model, "predict"):
        raise ModelLoadError("Loaded artifact does not implement predict()")
    logger.info("Loaded %s from %s", type(model).__name__, model_path)
    return model


def model_features(model: Any) -> list[str]:
    names = getattr(model, "feature_names_in_", None)
    if names is not None:
        return [str(name) for name in names]
    count = getattr(model, "n_features_in_", None)
    return [f"feature_{index + 1}" for index in range(int(count or 0))]
