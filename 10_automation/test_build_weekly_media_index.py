import csv
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_weekly_media_index import build_indexes


def write_png(path, width=900, height=1600):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = b"\x00" + (b"\x00\x00\x00" * width)
    data = raw * height

    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(data))
        + chunk(b"IEND", b"")
    )


def write_review(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["look_id", "candidate_file", "publishable", "status"])
        writer.writeheader()
        writer.writerows(rows)


class WeeklyMediaIndexTest(unittest.TestCase):
    def test_builds_two_ordered_five_source_reels(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temp:
            root = Path(temp)
            run_dir = root / "10_automation" / "runs" / "2026-W35"
            run_dir.mkdir(parents=True)
            fields = ["week_id", "carousel_id", "model_profile_id", "look_id", "look_order", "theme_name", "look_name"]
            with (run_dir / "weekly_look_plan.csv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                for theme in range(1, 6):
                    for order in (1, 2):
                        carousel_id = f"2026-W35-{theme:03d}"
                        look_id = f"{carousel_id}-L{order:02d}"
                        writer.writerow(
                            {
                                "week_id": "2026-W35",
                                "carousel_id": carousel_id,
                                "model_profile_id": f"M{theme:02d}",
                                "look_id": look_id,
                                "look_order": order,
                                "theme_name": f"Theme {theme}",
                                "look_name": f"Look {theme}-{order}",
                            }
                        )
                        look_dir = run_dir / "generated_images" / carousel_id / "looks" / look_id
                        reel_name = f"{look_id}_M{theme:02d}_reel_candidate_A.png"
                        write_png(look_dir / "reel" / reel_name)
                        write_review(
                            look_dir / "reel" / "review_sheet.csv",
                            [{"look_id": look_id, "candidate_file": reel_name, "publishable": "yes", "status": "user_approved"}],
                        )
                        carousel_rows = []
                        for role in "ABC":
                            name = f"{look_id}_M{theme:02d}_carousel_candidate_{role}.png"
                            write_png(look_dir / "carousel" / name, 1000, 1200)
                            carousel_rows.append(
                                {"look_id": look_id, "candidate_file": name, "publishable": "yes", "status": "user_approved"}
                            )
                        write_review(look_dir / "carousel" / "review_sheet.csv", carousel_rows)
                        ready = look_dir / "carousel" / "canva_ready"
                        ready.mkdir()
                        (ready / "canva_commit_record.json").write_text(
                            json.dumps(
                                {
                                    "transaction_status": "committed",
                                    "canva_design_id": f"DESIGN-{theme}-{order}",
                                    "canva_title": "Title",
                                    "canva_display_copy": "Copy",
                                    "canva_edit_url": "https://www.canva.com/d/edit",
                                    "canva_view_url": "https://www.canva.com/d/view",
                                    "transaction_id": "tx",
                                    "committed_at": "2026-08-27",
                                }
                            ),
                            encoding="utf-8",
                        )

            weekly, reel_manifest = build_indexes(
                run_dir=run_dir,
                project_root=root,
                repository="owner/repo",
                branch="main",
                updated_at="2026-08-27",
            )
            self.assertEqual(weekly["status"], "ready_for_reel_assembly_and_manual_export")
            self.assertEqual(weekly["progress"]["looks_ready_for_manual_export"], 10)
            self.assertEqual([reel["source_count"] for reel in reel_manifest["reels"]], [5, 5])
            self.assertTrue(all(source["look_id"].endswith("L01") for source in reel_manifest["reels"][0]["sources"]))
            self.assertTrue(all(source["look_id"].endswith("L02") for source in reel_manifest["reels"][1]["sources"]))
            self.assertIn("raw.githubusercontent.com/owner/repo/main/", reel_manifest["reels"][0]["sources"][0]["raw_url"])


if __name__ == "__main__":
    unittest.main()
