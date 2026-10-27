"""Record the exact user's acceptance without widening it into publication or format adoption."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OUTPUT = HERE / "review/M02_paired_D_v1_review_v2_matched.mp4"
EXPECTED = "3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    actual = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    if actual != EXPECTED:
        raise ValueError("Displayed output hash changed; do not transfer acceptance")
    approval = dict(
        date="2026-10-05", user_reply="ok", approval_source="direct user reply to latest complete M02 v2 preview",
        output_path=OUTPUT.relative_to(ROOT).as_posix(), output_sha256=actual,
        scope="accepted_clean_picture_track_for_this_exact_cut",
        seconds=11.25, frames=270, fps=24, resolution=[720, 1280],
        transition=dict(type="cross_dissolve", count=1, seconds=0.75, output_seconds=[5.25, 6]),
        text="none", audio="none", source_speed="unchanged",
        A_framing="fixed proportional scale747x1328; fixed crop720x1280x14y44", B_framing="original",
        user_detailed_rationale=None, user_full_watch_self_report=None, assistant_continuous_review=False,
        sampled_limitations_preserved=["residual face/hand/bag and background double edges", "opening top margin roughly2%at0.5s"],
        account_wide_format_adoption="not_inferred", audience_performance=None,
        cloud_upload_authorized_by_this_reply=False, publication_authorized_by_this_reply=False,
        status="accepted_clean_picture_track",
    )
    save(HERE / "user_video_approval_2026-10-05.json", approval)
    receipt_path = OUTPUT.with_suffix(".json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt.update(status="accepted_clean_picture_track", user_visual_approval=approval,
                   approval_record="../user_video_approval_2026-10-05.json",
                   release_status="clean_picture_accepted_IG_music_cover_safe_area_and_final_assembly_separate")
    # Retain technical-review fields and false publishable flag: acceptance of
    # this clean picture does not supply publication data or audio rights.
    save(receipt_path, receipt)
    board_path = HERE / "storyboard.json"
    board = json.loads(board_path.read_text(encoding="utf-8"))
    board.update(status="accepted_clean_picture_track", dynamic_qa="decode_and_sampled_QA_complete_user_exact_cut_accepted_assistant_continuous_review_not_claimed")
    board["actual_render"].update(user_approval="user_video_approval_2026-10-05.json", status="accepted_clean_picture_track")
    save(board_path, board)
    print(json.dumps(dict(status=approval["status"], hash_matches=True, output=approval["output_path"]), ensure_ascii=False))


if __name__ == "__main__":
    main()
