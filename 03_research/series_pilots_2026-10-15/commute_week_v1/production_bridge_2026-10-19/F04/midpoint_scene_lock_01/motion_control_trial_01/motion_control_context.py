"""Bound exact inputs for the approved midpoint-controlled F04 trial.

No media operation happens on import. All prior tools and media remain read-only.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
MIDPOINT = HERE.parent
F04 = MIDPOINT.parent
SOURCE = HERE / "F04_source.mp4"
REJECTED_SOURCES = {
    "d83c6c18fa7d058c3eb3b374afad70db0a51cf0c561ba2c6bd4a255041d0bb50",
    "25252192b6ce6052d88bd645fba47496246be59b23c953e5b3ad68f29ef11739",
}
BASE_BUILDER = F04 / "build_four_shot_review.py"
BASE_INSPECTOR = F04 / "inspect_F04_source.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load read-only helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


append = load("mira_midpoint_f04_append_base", BASE_BUILDER)
inspector = load("mira_midpoint_f04_inspect_base", BASE_INSPECTOR)
native = append.native
PROTECTED = [
    (append.PREFIX, append.PREFIX_SHA),
    (F04 / "F04_M03_L02_start_candidate_A.png", "98687eb8365828d67850ddc03d57e48d9d28ad4628f9f62c727bcb166e002457"),
    (MIDPOINT / "F04_M03_L02_midpoint_crosswalk90_v2.png", "25606eaac1e1bbd7f8e53873de07d2a2b99c87ace88924f1917cd94dae55175b"),
    (MIDPOINT / "end_crosswalk_alignment_01/F04_M03_L02_end_crosswalk_candidate_A.png", "c7ceec64741262645fd5a59339d5cece3162fe8d928f7a0e0dd7521ace1b0d14"),
]


def require_new_source(digest):
    if digest in REJECTED_SOURCES:
        raise ValueError("Rejected prior failed F04 source; require the newly downloaded midpoint-control trial source")
    native.verified_source(SOURCE, digest)
    for path, expected in PROTECTED:
        native.verified_source(path, expected)


def provenance(output, sha, wrapper):
    wrapper = Path(wrapper).resolve()
    native.json_new(output / "motion_control_execution.json", {
        "created_at_taipei": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "context": str(Path(__file__).resolve()), "context_sha256": native.sha256(Path(__file__).resolve()),
        "wrapper": str(wrapper), "wrapper_sha256": native.sha256(wrapper),
        "borrowed_builder": str(BASE_BUILDER), "borrowed_builder_sha256": native.sha256(BASE_BUILDER),
        "borrowed_inspector": str(BASE_INSPECTOR), "borrowed_inspector_sha256": native.sha256(BASE_INSPECTOR),
        "source": str(SOURCE), "source_sha256": sha,
        "protected_inputs": [{"path": str(path), "sha256": digest} for path, digest in PROTECTED],
        "rejected_previous_source_sha256": sorted(REJECTED_SOURCES),
        "requested_midpoint_control_is_not_proof_of_generator_settings": True,
        "new_source_visual_qa_pass": None, "normal_speed_full_playback": None,
        "user_video_approval": None, "publishable": False,
    })


def inspect(sha, version, wrapper):
    require_new_source(sha)
    inspector.HERE = HERE
    # Inspector uses this module only for PROTECTED and native stream/hash tools.
    class Configuration:
        pass
    config = Configuration()
    config.PROTECTED = PROTECTED
    config.native = native
    inspector.builder = config
    result = inspector.inspect(sha, version)
    require_new_source(sha)
    provenance(Path(result["output_QA"]), sha, wrapper)
    return result


def build(sha, version, wrapper):
    require_new_source(sha)
    append.HERE = HERE
    append.SOURCE = SOURCE
    append.PROTECTED = PROTECTED
    result = append.build(sha, version)
    require_new_source(sha)
    provenance(Path(result["output"]).parent, sha, wrapper)
    return result
