import json
from pathlib import Path


MODEL_IDS = {"M01", "M02", "M03", "M04"}

MODEL_ROTATION = ["M01", "M02", "M03", "M04"]


def clean(value):
    return " ".join(str(value or "").split()).strip()


def model_for_index(index):
    """Rotate age cohorts so any outfit category can be styled for multiple ages."""
    try:
        numeric_index = int(index)
    except (TypeError, ValueError):
        numeric_index = 1
    return MODEL_ROTATION[(max(numeric_index, 1) - 1) % len(MODEL_ROTATION)]


def model_for_bucket(content_bucket):
    # Backward-compatible fallback only. New weekly packet builds use model_for_index.
    return "M04"


def load_model_roster(path="02_brand/mira_model_roster.json"):
    roster_path = Path(path)
    if not roster_path.exists():
        return {}
    data = json.loads(roster_path.read_text(encoding="utf-8"))
    return {clean(profile.get("model_profile_id")): profile for profile in data.get("profiles", [])}


def validate_model_id(model_profile_id):
    value = clean(model_profile_id)
    return value if value in MODEL_IDS else ""
