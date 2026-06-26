import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_INDEX_URL = "https://mika-lin-weekly.pplx.app/data/index.json"


def clean(value):
    return " ".join(str(value or "").split()).strip()


def read_text(source):
    if re.match(r"^https?://", source):
        request = urllib.request.Request(source, headers={"User-Agent": "MikaLinPipeline/1.0"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8-sig", errors="replace")
    return Path(source).read_text(encoding="utf-8-sig")


def absolutize(base_url, value):
    value = clean(value)
    if not value:
        return ""
    if re.match(r"^https?://", value):
        return value
    return urllib.parse.urljoin(base_url, value)


def row_week(row):
    for key in ["week", "week_id", "id", "slug"]:
        value = clean(row.get(key))
        if value:
            return value
    return ""


def row_csv_url(row, base_url):
    for key in ["csv_url", "data_url", "csv", "machine_readable_url", "export_url"]:
        value = clean(row.get(key))
        if value:
            return absolutize(base_url, value)

    week = row_week(row)
    if week:
        return urllib.parse.urljoin(base_url, f"/data/{week}.csv")
    return ""


def normalize_index_payload(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ["weeks", "items", "reports", "data"]:
            value = payload.get(key)
            if isinstance(value, list):
                return value
        if payload:
            return [payload]
    return []


def sort_key(row):
    week = row_week(row)
    date_value = clean(row.get("date") or row.get("created_at") or row.get("updated_at"))
    return (date_value, week)


def resolve_source(index_source=DEFAULT_INDEX_URL, week="", latest=True):
    text = read_text(index_source)
    payload = json.loads(text)
    rows = normalize_index_payload(payload)
    if not rows:
        raise ValueError("Perplexity index did not contain any weekly report rows.")

    if week:
        matches = [row for row in rows if row_week(row) == week]
        if not matches:
            raise ValueError(f"Week not found in Perplexity index: {week}")
        selected = matches[0]
    elif latest:
        selected = sorted(rows, key=sort_key, reverse=True)[0]
    else:
        selected = rows[0]

    csv_url = row_csv_url(selected, index_source)
    if not csv_url:
        raise ValueError("Selected Perplexity index row did not include or imply a CSV URL.")

    return {
        "week": row_week(selected),
        "csv_url": csv_url,
        "source": index_source,
        "row": selected,
    }


def main():
    parser = argparse.ArgumentParser(description="Resolve the latest Perplexity weekly CSV URL from the public index.")
    parser.add_argument("--index", default=DEFAULT_INDEX_URL)
    parser.add_argument("--week", default="")
    parser.add_argument("--latest", action="store_true", default=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = resolve_source(index_source=args.index, week=args.week, latest=args.latest)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["csv_url"])


if __name__ == "__main__":
    main()
