import argparse
import base64
import csv
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-1")
DEFAULT_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

INVENTORY_FIELDS = [
    "prompt_id",
    "file_name",
    "file_path",
    "provider",
    "model",
    "size",
    "quality",
    "variant",
    "status",
    "notes",
]

SCORE_FIELDS = [
    "prompt_id",
    "file_name",
    "tool",
    "identity_consistency",
    "outfit_clarity",
    "body_integrity",
    "platform_fit",
    "shopping_value",
    "publishable",
    "best_platform",
    "status",
    "notes",
]


def clean(value):
    return " ".join((value or "").split()).strip()


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_identity_block(path):
    path = Path(path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def build_prompt(packet, identity_block=""):
    identity = """
Mira is a fictional AI virtual fashion creator for Taiwan Traditional Chinese audiences.
Taiwanese woman in her late 20s, soft oval face, natural warm fair skin, deep brown hair,
clean natural makeup, slim healthy proportions, calm friendly city style.
""".strip()
    if identity_block:
        identity = identity_block

    return f"""Create a vertical fashion social media image for an AI virtual creator.

Stable fictional identity:
{identity}

Outfit:
- Clothing item: {clean(packet.get("clothing_item"))}
- Color palette: {clean(packet.get("color_palette"))}
- Fabric: {clean(packet.get("fabric"))}
- Fit: {clean(packet.get("fit"))}
- Styling rules: {clean(packet.get("styling_rules"))}
- Occasion: {clean(packet.get("occasion"))}
- Scene: {clean(packet.get("scene"))}

Composition:
- Full outfit visible from head to shoes.
- Practical Taiwan daily-life setting.
- Realistic natural light.
- Clean composition for Instagram carousel.
- Clothing structure must be easy to inspect on a phone screen.

Safety and brand rules:
- Fictional AI virtual outfit only.
- No real person likeness.
- No celebrity likeness.
- No childlike appearance.
- No school uniform.
- No nudity or sexualized pose.
- No visible logos, luxury brand marks, signage, watermark, or text on image.
- Avoid distorted hands, extra fingers, warped legs, and unreadable clothing details.
"""


def request_image(api_key, api_base, payload, timeout):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{api_base.rstrip('/')}/images/generations",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI image request failed: HTTP {exc.code}: {body}") from exc


def decode_image(item):
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=120) as response:
            return response.read()
    raise RuntimeError("OpenAI image response did not include b64_json or url.")


def write_review_template(path, inventory_rows):
    rows = []
    for item in inventory_rows:
        row = {field: "" for field in SCORE_FIELDS}
        row["prompt_id"] = item["prompt_id"]
        row["file_name"] = item["file_name"]
        row["tool"] = "OpenAI"
        row["publishable"] = "pending"
        row["status"] = "review"
        rows.append(row)
    write_csv(path, SCORE_FIELDS, rows)


def generate_images(
    run_dir,
    model=DEFAULT_MODEL,
    size="1024x1536",
    quality="medium",
    variants=2,
    output_format="png",
    dry_run=False,
    api_base=DEFAULT_API_BASE,
    identity_path="02_brand/mira_identity_block.md",
    timeout=180,
    delay_seconds=1.0,
):
    run_dir = Path(run_dir)
    packet_path = run_dir / "weekly_content_packet.csv"
    if not packet_path.exists():
        raise SystemExit(f"Missing weekly content packet: {packet_path}")

    packets = read_csv(packet_path)
    identity_block = load_identity_block(identity_path)
    images_dir = run_dir / "openai_images"
    images_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir = run_dir / "openai_prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not dry_run and not api_key:
        raise SystemExit("OPENAI_API_KEY is required unless --dry-run is used.")

    inventory_rows = []
    extension = "png" if output_format.lower() == "png" else "jpg"

    for packet in packets:
        prompt_id = clean(packet.get("prompt_id"))
        carousel_id = clean(packet.get("carousel_id"))
        prompt = build_prompt(packet, identity_block=identity_block)
        (prompt_dir / f"{prompt_id}.txt").write_text(prompt, encoding="utf-8")

        for variant in range(1, variants + 1):
            file_name = f"{prompt_id}_openai_v{variant}.{extension}"
            file_path = images_dir / file_name
            notes = f"carousel_id={carousel_id}; prompt_file=openai_prompts/{prompt_id}.txt"

            if dry_run:
                status = "planned"
            else:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "size": size,
                    "quality": quality,
                    "n": 1,
                }
                if output_format:
                    payload["output_format"] = output_format
                response = request_image(api_key, api_base, payload, timeout=timeout)
                image_items = response.get("data", [])
                if not image_items:
                    raise RuntimeError(f"No image returned for {prompt_id} variant {variant}.")
                file_path.write_bytes(decode_image(image_items[0]))
                status = "generated"
                time.sleep(delay_seconds)

            inventory_rows.append(
                {
                    "prompt_id": prompt_id,
                    "file_name": file_name,
                    "file_path": str(file_path),
                    "provider": "openai",
                    "model": model,
                    "size": size,
                    "quality": quality,
                    "variant": variant,
                    "status": status,
                    "notes": notes,
                }
            )

    write_csv(run_dir / "openai_image_inventory.csv", INVENTORY_FIELDS, inventory_rows)
    write_review_template(run_dir / "openai_asset_review_template.csv", inventory_rows)
    return inventory_rows


def main():
    parser = argparse.ArgumentParser(description="Generate OpenAI image assets for a Mira weekly run.")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default="1024x1536")
    parser.add_argument("--quality", default="medium")
    parser.add_argument("--variants", type=int, default=2)
    parser.add_argument("--output-format", default="png", choices=["png", "jpeg", "webp"])
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--identity-path", default="02_brand/mira_identity_block.md")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--delay-seconds", type=float, default=1.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = generate_images(
        run_dir=args.run_dir,
        model=args.model,
        size=args.size,
        quality=args.quality,
        variants=args.variants,
        output_format=args.output_format,
        dry_run=args.dry_run,
        api_base=args.api_base,
        identity_path=args.identity_path,
        timeout=args.timeout,
        delay_seconds=args.delay_seconds,
    )
    action = "Planned" if args.dry_run else "Generated"
    print(f"{action} {len(rows)} OpenAI image asset(s).")
    print(f"Wrote {Path(args.run_dir) / 'openai_image_inventory.csv'}")
    print(f"Wrote {Path(args.run_dir) / 'openai_asset_review_template.csv'}")


if __name__ == "__main__":
    main()
