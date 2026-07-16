import json
from pathlib import Path


REGISTRY_PATH = Path(__file__).with_name("canva_template_registry.json")


def clean(value):
    return " ".join(str(value or "").split()).strip()


def load_template_registry(path=REGISTRY_PATH):
    path = Path(path)
    if not path.exists():
        return {}
    registry = json.loads(path.read_text(encoding="utf-8"))
    return {
        clean(template.get("key")).upper(): template
        for template in registry.get("templates", [])
        if clean(template.get("key"))
    }


def choose_template(packet, templates):
    if not templates:
        return {}

    explicit = clean(packet.get("canva_template_key") or packet.get("template_key")).upper()
    if explicit in templates:
        return templates[explicit]

    blob = " ".join(
        clean(packet.get(field))
        for field in [
            "trend_name",
            "content_bucket",
            "audience",
            "occasion",
            "clothing_item",
            "color_palette",
            "fabric",
            "fit",
            "styling_rules",
            "scene",
        ]
    ).lower()

    keyword_rules = [
        ("C", ["noir", "evening", "night", "autumn", "winter", "晚宴", "夜", "夜晚", "秋冬", "秋", "冬", "低光"]),
        ("B", ["office", "commute", "formal", "tailored", "blazer", "通勤", "上班", "正式", "剪裁", "西外", "西裝"]),
        ("E", ["weekend", "linen", "cafe", "airy", "週末", "假日", "亞麻", "咖啡", "留白"]),
        ("D", ["full-bleed", "hero image", "image-led", "strong visual", "大片", "強視覺", "滿版"]),
    ]
    for key, keywords in keyword_rules:
        if key in templates and any(keyword in blob for keyword in keywords):
            return templates[key]
    return templates.get("A") or next(iter(templates.values()))


def slot_for_variant(template, variant):
    slot_id = {"A": "cover_image", "B": "motion_crop", "C": "detail_image"}[variant]
    slot = dict(template.get("slot_geometry", {}).get(slot_id, {}))
    slot["slot_id"] = slot_id
    slot["variant"] = variant
    return slot

