from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = [ROOT / "best_model.pkl", ROOT / "model.pkl", ROOT / "notebook" / "best_model.pkl", ROOT / "notebook" / "model.pkl"]
DESTINATION = ROOT / "backend" / "model.pkl"

source = next((path for path in CANDIDATES if path.exists() and path.is_file()), None)
if source is None:
    searched = "\n".join(f"- {path}" for path in CANDIDATES)
    raise FileNotFoundError(f"No trained model found. Execute the notebook export cell first. Searched:\n{searched}")
DESTINATION.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, DESTINATION)
print(f"Exported {source} -> {DESTINATION}")
