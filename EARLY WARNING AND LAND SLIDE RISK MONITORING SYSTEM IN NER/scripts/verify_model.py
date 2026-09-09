from pathlib import Path
import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "backend" / "model.pkl"
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Missing {MODEL_PATH}. Run scripts/export_model.py first.")

model = joblib.load(MODEL_PATH)
features = [str(value) for value in getattr(model, "feature_names_in_", [])]
feature_count = int(getattr(model, "n_features_in_", len(features)))
print(f"Model type: {type(model).__name__}")
print(f"Feature count: {feature_count}")
print(f"Feature names: {features or '[not stored by estimator]'}")

sample = np.zeros((1, feature_count), dtype=float)
if hasattr(model, "predict_proba"):
    result = model.predict_proba(sample).tolist()
else:
    result = model.predict(sample).tolist()
print(f"Sample prediction: {result}")
