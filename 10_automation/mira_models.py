import json
import random
from pathlib import Path


MODEL_ROTATION = ["M01", "M02", "M03", "M04", "M05"]

MODEL_IDS = set(MODEL_ROTATION)

LOCKED_WEEK_MODEL_ORDERS = {
    # W27 already published item 001 as M01, so keep the visible sequence stable.
    "2026-W27": MODEL_ROTATION,
}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def model_order_for_week(week_id=None):
    """Return a deterministic weekly model order that uses each internal model once."""
    week_key = clean(week_id)
    if week_key in LOCKED_WEEK_MODEL_ORDERS:
        return list(LOCKED_WEEK_MODEL_ORDERS[week_key])
    if not week_key:
        return list(MODEL_ROTATION)

    order = list(MODEL_ROTATION)
    random.Random(f"{week_key}:mira-model-weekly-v1").shuffle(order)
    return order


def model_for_index(index, week_id=None):
    """Assign each weekly carousel a model, cycling only after all five are used."""
    try:
        numeric_index = int(index)
    except (TypeError, ValueError):
        numeric_index = 1
    order = model_order_for_week(week_id)
    return order[(max(numeric_index, 1) - 1) % len(order)]


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
