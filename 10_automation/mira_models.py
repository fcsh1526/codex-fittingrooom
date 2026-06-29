import json
from pathlib import Path


MODEL_IDS = {"M01", "M02", "M03"}

BUCKET_TO_MODEL = {
    "office_capsule": "M01",
    "date_outfit": "M02",
    "weekend_daily": "M02",
    "daily_style": "M03",
    "rainy_day": "M03",
}


def clean(value):
    return " ".join(str(value or "").split()).strip()


def model_for_bucket(content_bucket):
    return BUCKET_TO_MODEL.get(clean(content_bucket), "M03")


def load_model_roster(path="02_brand/mira_model_roster.json"):
    roster_path = Path(path)
    if not roster_path.exists():
        return {}
    data = json.loads(roster_path.read_text(encoding="utf-8"))
    return {clean(profile.get("model_profile_id")): profile for profile in data.get("profiles", [])}


def validate_model_id(model_profile_id):
    value = clean(model_profile_id)
    return value if value in MODEL_IDS else ""
