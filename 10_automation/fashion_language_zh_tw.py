import re


TERM_RULES = [
    (r"卡普里褲|\bCapri(?:\s+Pants?)?\b", "七分褲"),
    (r"Fisherman\s*涼鞋|\bFisherman(?:\s+Sandals?)?\b", "漁夫涼鞋"),
    (r"\b(?:wide[- ]leg(?:ged)?|wide)\s+(?:trousers|pants)\b", "寬褲"),
    (r"\bSheer\s+Layering\b", "透膚疊穿"),
    (r"\bButter\s+Yellow\b", "奶油黃"),
    (r"\bScarf[- ]as[- ]Belt\b", "絲巾腰帶"),
]


def clean(value):
    return " ".join(str(value or "").split()).strip()


def localize_display_text(value):
    text = clean(value)
    for pattern, replacement in TERM_RULES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Remove English/source parentheses after the localized term is already present.
    text = re.sub(r"（\s*(七分褲|漁夫涼鞋|透膚疊穿|奶油黃|絲巾腰帶)\s*）", "", text)
    text = re.sub(r"\(\s*(七分褲|漁夫涼鞋|透膚疊穿|奶油黃|絲巾腰帶)\s*\)", "", text)
    text = text.replace("+", "＋")
    text = re.sub(r"\s*/\s*", "與", text)
    return clean(text)


def localize_packet_fields(row):
    localized = dict(row)
    for field in ["trend_name", "clothing_item", "occasion", "audience"]:
        localized[field] = localize_display_text(localized.get(field, ""))
    return localized


def display_mood_line(row):
    item = localize_display_text(row.get("clothing_item", ""))
    trend = localize_display_text(row.get("trend_name", ""))

    recipes = [
        ("七分褲", "Clean Lines.\nCity Rhythm."),
        ("漁夫涼鞋", "Light Steps.\nOpen Roads."),
        ("奶油黃", "Butter Light.\nWorkday Ease."),
        ("絲巾腰帶", "A Silk Twist.\nWeekend Denim."),
        ("透膚", "Soft Layers.\nQuiet Confidence."),
    ]
    searchable = f"{trend} {item}"
    for keyword, line in recipes:
        if keyword in searchable:
            return line

    return "Everyday Ease.\nStyled with Intent."
