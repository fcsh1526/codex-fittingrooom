import re


TERM_RULES = [
    (r"卡普里褲|\bCapri(?:\s+Pants?)?\b", "七分褲"),
    (r"Fisherman\s*涼鞋|\bFisherman(?:\s+Sandals?)?\b", "漁夫涼鞋"),
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
        ("七分褲", "七分褲配簡潔上衣\n城市散步也俐落"),
        ("漁夫涼鞋", "漁夫涼鞋搭寬褲\n旅行走路也輕盈"),
        ("奶油黃", "奶油黃疊穿\n通勤清爽有精神"),
        ("絲巾腰帶", "絲巾腰帶點亮牛仔褲\n週末穿搭更有層次"),
        ("透膚", "透膚材質輕輕疊穿\n通勤也不顯單調"),
    ]
    searchable = f"{trend} {item}"
    for keyword, line in recipes:
        if keyword in searchable:
            return line

    subject = item or trend or "簡潔穿搭"
    subject = subject[:12]
    return f"{subject}\n日常穿得更有層次"
