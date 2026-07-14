import re


TERM_RULES = [
    (r"浪漫\s+Boho[- ]Romantic\s*[（(]\s*Lace\s*[/、與,]\s*Fringe\s*[/、與,]\s*Embroidery\s*[）)]", "浪漫波西米亞（蕾絲、流蘇與刺繡）"),
    (r"未完成剪裁\s*/\s*解構\s+Tailoring\s*[（(]\s*Exposed\s+Stitch\s*/\s*Asymmetry\s*[）)]", "未完成剪裁與解構西裝（外露車線與不對稱）"),
    (r"鬆弛輪廓\s+Relaxed\s+Utility\s*[（(]\s*Barrel\s*/\s*Volume\s+Pants\s*[）)]", "鬆弛實用輪廓（氣球褲與寬量感下身）"),
    (r"色彩點亮\s+Color\s+Pop\s+on\s+Neutrals\s*[（(]\s*Mint\s*/\s*Butter\s*/\s*Primary\s*[）)]", "中性色彩亮點（薄荷綠、奶油黃與原色）"),
    (r"\s*[（(]\s*Airy\s+Edit\s*[）)]", ""),
    (r"\bBoho[- ]Romantic\b", "浪漫波西米亞"),
    (r"[（(]\s*Lace與Fringe與Embroidery\s*[）)]", "（蕾絲、流蘇與刺繡）"),
    (r"卡普里褲|\bCapri(?:\s+Pants?)?\b", "七分褲"),
    (r"Fisherman\s*涼鞋|\bFisherman(?:\s+Sandals?)?\b", "漁夫涼鞋"),
    (r"\bchiffon\s+overlay\s+dress\s+layered\s+over\s+slip\s+dress\b", "雪紡罩衫洋裝＋細肩帶內搭洋裝"),
    (r"\borganza\s+shirt\s+as\s+light\s+jacket\b", "歐根紗襯衫式薄外套"),
    (r"\bsheer\s+mesh\s+long[- ]sleeve\s+top\b", "透膚網紗長袖上衣"),
    (r"\blace[- ]trim\s+cami\b", "蕾絲滾邊細肩帶背心"),
    (r"\bdeconstructed\s+blazer\b", "解構西裝外套"),
    (r"\bshort\s+blazer\b", "短版西裝外套"),
    (r"\bbutter[- ]yellow\s+cardigan\b", "奶油黃開襟衫"),
    (r"\bsatin\s+cami\b", "緞面細肩帶背心"),
    (r"\bribbed\s+tank\b", "羅紋背心"),
    (r"\bsheer\s+cardigan\b", "透膚開襟衫"),
    (r"\bsheer\s+top\b", "透膚上衣"),
    (r"\bbra\s+top\b", "短版內搭"),
    (r"\bfitted\s+tank\b", "合身背心"),
    (r"\bwhite\s+tank\b", "白色背心"),
    (r"\bbarrel\s+jeans\b", "氣球版型牛仔褲"),
    (r"\bstraight\s+trousers\b", "直筒長褲"),
    (r"\bmidi\s+skirt\b", "中長裙"),
    (r"\b(?:wide[- ]leg(?:ged)?|wide)\s+(?:trousers|pants)\b", "寬褲"),
    (r"\blinen\b", "亞麻"),
    (r"\bwoven\s+bag\b", "編織包"),
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
    text = text.replace("浪漫 浪漫波西米亞", "浪漫波西米亞")
    text = text.replace("亞麻 寬褲", "亞麻寬褲")
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
