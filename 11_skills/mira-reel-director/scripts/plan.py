#!/usr/bin/env python3
"""Create/check a Mira directing plan. No media generation or visual QA."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path, PureWindowsPath
import re
import sys

LAYOUTS = {"single_sequential", "parallel_comparison", "primary_detail"}
RECIPES = {"sequential_lookbook", "parallel_comparison", "everyday_sequence",
           "foreground_reveal", "continuous_route", "single_shot_performance",
           "primary_detail_experiment", "overhead_fan_transition_experiment", "custom_experiment"}
SHA = re.compile(r"^[0-9a-f]{64}$")
WEEK = re.compile(r"^\d{4}-W(?:0[1-9]|[1-4]\d|5[0-3])$")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


def vector(value, n=3):
    return isinstance(value, list) and len(value) == n and all(number(x) for x in value)


class Check:
    def __init__(self, plan, path, project_root=None):
        self.p = plan
        self.path = Path(path).resolve()
        self.errors, self.missing, self.warnings = [], [], []
        self.assets, self.files, self.hashes = {}, {}, {}
        self.base = self.path.parent
        if plan.get("path_base") == "project":
            if project_root is None:
                self.errors.append("project path_base requires --project-root")
            else:
                self.base = Path(project_root).resolve()
        elif plan.get("path_base") != "plan":
            self.errors.append("path_base must be plan or project")

    def require(self, value, message):
        if value is None or value == "" or value == [] or value == {}:
            self.missing.append(message)
            return False
        return True

    def records(self, container, key):
        value = container.get(key, [])
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            self.errors.append(f"{key} must be an array of objects")
            return []
        return value

    def interval(self, value, label, allow_zero=False):
        if (not isinstance(value, list) or len(value) != 2 or
                not all(integer(x) for x in value) or value[0] < 0 or
                (value[1] < value[0] if allow_zero else value[1] <= value[0])):
            self.errors.append(f"{label}: invalid half-open frame interval")
            return None
        return tuple(value)

    def local_path(self, value, label):
        if not self.require(value, f"{label}: missing path"):
            return None
        if not isinstance(value, str):
            self.errors.append(f"{label}: path must be a string")
            return None
        relative = Path(value)
        if relative.is_absolute() or PureWindowsPath(value).drive or ".." in relative.parts or "\\" in value:
            self.errors.append(f"{label}: use forward-slash relative paths inside path_base")
            return None
        result = (self.base / relative).resolve()
        if not result.is_relative_to(self.base):
            self.errors.append(f"{label}: resolved path escapes path_base")
            return None
        if not result.is_file():
            self.missing.append(f"{label}: file absent: {value}")
            return None
        return result

    def asset_ref(self, aid, label, kind=None):
        if not self.require(aid, f"{label}: missing asset ID"):
            return None
        asset = self.assets.get(aid)
        if asset is None:
            self.errors.append(f"{label}: unknown asset {aid}")
        elif kind and asset.get("kind") not in kind:
            self.errors.append(f"{label}: asset kind must be one of {sorted(kind)}")
        return asset

    def approval(self, aid, scope):
        if not aid or aid not in self.assets:
            return
        candidates = [x for x in self.records(self.p, "approvals")
                      if x.get("asset_id") == aid and x.get("scope") == scope and
                      x.get("decision") == "approved"]
        actual = self.hashes.get(aid)
        for record in candidates:
            receipt = self.local_path(record.get("receipt_path"), f"approval {aid}/{scope}")
            if not receipt or not actual:
                continue
            if record.get("target_sha256") != actual:
                self.errors.append(f"approval {aid}/{scope}: stale target SHA256")
                continue
            try:
                evidence = json.loads(receipt.read_text(encoding="utf-8-sig"))
            except (ValueError, OSError) as exc:
                self.errors.append(f"approval {aid}/{scope}: receipt is not readable JSON ({type(exc).__name__})")
                continue
            if (isinstance(evidence, dict) and evidence.get("actor") == "user" and
                    evidence.get("decision") == "approved" and evidence.get("scope") == scope and
                    evidence.get("target_sha256") == actual and
                    isinstance(evidence.get("quote"), str) and evidence["quote"].strip() and
                    isinstance(evidence.get("recorded_at"), str) and evidence["recorded_at"].strip()):
                return
            self.errors.append(f"approval {aid}/{scope}: receipt fields do not evidence exact user approval")
        self.missing.append(f"{aid}: user {scope} approval evidence required")

    def inspect_assets(self):
        for asset in self.records(self.p, "assets"):
            aid = asset.get("id")
            if not isinstance(aid, str) or not aid:
                self.errors.append("asset ID must be a nonempty string")
                continue
            if aid in self.assets:
                self.errors.append(f"duplicate asset ID {aid}")
            self.assets[aid] = asset
            path = self.local_path(asset.get("path"), f"asset {aid}")
            if path:
                self.files[aid], self.hashes[aid] = path, digest(path)
                expected = asset.get("sha256")
                if not expected:
                    self.missing.append(f"asset {aid}: record SHA256")
                elif expected != self.hashes[aid]:
                    self.errors.append(f"asset {aid}: SHA256 mismatch")
        for item in self.p.get("missing_assets", []):
            self.missing.append(f"declared missing asset: {item}")

    def inspect_frame_reuse(self, aid, asset):
        lineage = asset.get("lineage", {})
        authority = asset.get("reuse_authority", {})
        source_id = lineage.get("source_asset_id")
        source = self.asset_ref(source_id, f"frame extract {aid} source", {"source_clip"})
        if source:
            if not self.hashes.get(source_id) or lineage.get("source_sha256") != self.hashes.get(source_id):
                self.errors.append(f"frame extract {aid}: source SHA256 missing/stale")
            index, count = lineage.get("frame_index"), source.get("frame_count")
            if not integer(index) or index < 0 or not integer(count) or count <= index:
                self.errors.append(f"frame extract {aid}: frame index outside known source frame_count")
        if not self.hashes.get(aid) or lineage.get("extracted_sha256") != self.hashes.get(aid):
            self.errors.append(f"frame extract {aid}: extracted frame SHA256 missing/stale")
        scope = authority.get("source_approval_scope")
        if self.require(scope, f"frame extract {aid}: original source approval scope missing"):
            self.approval(source_id, scope)
        self.local_path(authority.get("evidence_path"), f"frame extract {aid} reuse authority")
        self.require(authority.get("purpose"), f"frame extract {aid}: reuse purpose missing")

    def inspect_editorial(self):
        for key in ("plan_id", "status"):
            self.require(self.p.get(key), f"missing {key}")
        if self.p.get("status") not in {"draft", "in_review", "approved_for_generation"}:
            self.errors.append("status must be draft, in_review or approved_for_generation")
        ed = self.p.get("editorial", {})
        for key in ("audience", "takeaway", "visual_theme", "selection_rationale"):
            self.require(ed.get(key), f"editorial.{key} is incomplete")
        presentation = self.p.get("presentation", {})
        if presentation.get("layout_id") not in LAYOUTS:
            self.errors.append("unknown layout_id")
        if presentation.get("recipe_id") not in RECIPES:
            self.errors.append("unknown recipe_id")
        if presentation.get("recipe_id") == "custom_experiment":
            for key in ("recipe_name", "viewer_mechanism", "evidence_status"):
                self.require(presentation.get(key), f"presentation.{key} is required for custom_experiment")
        weeks = self.p.get("weeks", {})
        if not isinstance(weeks.get("source"), list):
            self.errors.append("weeks.source must be a list")
        else:
            self.require(weeks["source"], "source weeks missing")
            for week in weeks["source"]:
                if not isinstance(week, str) or not WEEK.fullmatch(week):
                    self.errors.append("invalid source week")
        for key in ("content", "delivery"):
            week = weeks.get(key)
            if week is not None and (not isinstance(week, str) or not WEEK.fullmatch(week)):
                self.errors.append(f"invalid {key} week")
        self.require(weeks.get("content"), "content week missing; do not substitute latest delivery week")
        # Delivery may legitimately be unknown until a film is approved.
        self.models, self.looks = {}, {}
        for model in self.records(self.p, "models"):
            mid = model.get("id")
            if not isinstance(mid, str) or not mid or mid in self.models:
                self.errors.append("model IDs must be unique nonempty strings")
                continue
            self.models[mid] = model
            refs = model.get("identity_asset_ids", [])
            self.require(refs, f"model {mid}: missing identity references")
            for aid in refs:
                self.asset_ref(aid, f"model {mid}", {"identity"})
                self.approval(aid, "identity")
        for look in self.records(self.p, "looks"):
            lid = look.get("id")
            if not isinstance(lid, str) or not lid or lid in self.looks:
                self.errors.append("look IDs must be unique nonempty strings")
                continue
            self.looks[lid] = look
            if look.get("model_id") not in self.models:
                self.errors.append(f"look {lid}: unknown model")
            self.require(look.get("wardrobe_summary"), f"look {lid}: wardrobe summary missing")
            refs = look.get("source_asset_ids", [])
            self.require(refs, f"look {lid}: source evidence missing")
            for aid in refs:
                self.asset_ref(aid, f"look {lid} source")
        self.require(self.models, "no models")
        self.require(self.looks, "no looks")

    def inspect_clip_inputs(self, shot, span, fps):
        """Check declared native-speed video reuse, including each parallel panel."""
        sid = shot.get("id")
        clips = self.records(shot, "clip_inputs")
        self.require(clips, f"shot {sid}: reuse_clip needs source video intervals")
        panels = {}
        raw_intervals = {}
        for clip in clips:
            aid = clip.get("asset_id")
            asset = self.asset_ref(aid, f"shot {sid} clip", {"source_clip"})
            source_span = self.interval(clip.get("source_frames"), f"shot {sid} source clip {aid}")
            output_span = self.interval(clip.get("output_frames"), f"shot {sid} clip output")
            panel = clip.get("panel_id", "full")
            if not isinstance(panel, str) or not panel:
                self.errors.append(f"shot {sid}: clip panel_id must be a nonempty string")
                continue
            if output_span:
                panels.setdefault(panel, []).append(output_span)
                if span and (output_span[0] < span[0] or output_span[1] > span[1]):
                    self.errors.append(f"shot {sid}: reused clip exceeds shot interval")
            if not asset:
                continue
            count, source_fps = asset.get("frame_count"), asset.get("fps")
            if not integer(count) or count <= 0:
                self.missing.append(f"source clip {aid}: actual frame_count required")
            elif source_span and source_span[1] > count:
                self.errors.append(f"shot {sid}: source clip {aid} is too short for requested interval")
            if not number(source_fps) or source_fps <= 0:
                self.missing.append(f"source clip {aid}: actual fps required")
            elif source_fps != fps:
                self.errors.append(f"shot {sid}: clip/film fps differ; this native-frame contract does not retime")
            if source_span and output_span and source_span[1]-source_span[0] != output_span[1]-output_span[0]:
                self.errors.append(f"shot {sid}: native clip source and output durations differ")
            if source_span:
                raw_intervals.setdefault((panel, aid), []).append(source_span)
            authority = clip.get("reuse_authority", {})
            self.local_path(authority.get("evidence_path"), f"shot {sid} clip reuse evidence")
            self.require(authority.get("purpose"), f"shot {sid}: clip reuse purpose required")
            # Evidence may be an approved final film plus EDL covering the source interval.
            # Do not fabricate separate approval of the entire raw clip.
        expected_panels = shot.get("panel_ids", ["full"])
        if not isinstance(expected_panels, list) or not expected_panels or any(not isinstance(x, str) for x in expected_panels):
            self.errors.append(f"shot {sid}: panel_ids must list the intended output panels")
            expected_panels = []
        if set(panels) != set(expected_panels):
            self.errors.append(f"shot {sid}: clip coverage must include exactly the planned panels")
        if span:
            for panel, ranges in panels.items():
                cursor = span[0]
                for start, end in sorted(ranges):
                    if start != cursor:
                        self.errors.append(f"shot {sid}/{panel}: reused clip gap or overlap")
                    cursor = end
                if cursor != span[1]:
                    self.errors.append(f"shot {sid}/{panel}: source footage does not cover the full shot")
        for (panel, aid), ranges in raw_intervals.items():
            ordered = sorted(ranges)
            if any(b[0] < a[1] for a, b in zip(ordered, ordered[1:])):
                self.errors.append(f"shot {sid}/{panel}: repeated source frames from {aid}; no looping to fill duration")

    def inspect_timeline(self):
        film = self.p.get("film", {})
        fps, total = film.get("fps"), film.get("frame_count")
        if not number(fps) or fps <= 0:
            self.errors.append("film.fps must be positive")
        if not integer(total) or total < 0:
            self.errors.append("film.frame_count must be a nonnegative integer")
            total = 0
        if not total:
            self.missing.append("film duration not planned")
        seconds = film.get("duration_seconds")
        if seconds is not None and number(fps) and fps > 0 and (not number(seconds) or abs(seconds - total/fps) > 0.00001):
            self.errors.append("duration_seconds differs from frame_count / fps")
        if film.get("native_speed") is not True:
            self.errors.append("film.native_speed must be true")
        if film.get("baked_text") is not False:
            self.errors.append("film.baked_text must be false")
        if film.get("aspect_ratio") != "9:16":
            self.errors.append("film.aspect_ratio must be 9:16")
        shots = self.records(self.p, "shots")
        self.require(shots, "no shots planned")
        self.shots, spans, reads = {}, {}, {}
        for shot in shots:
            sid = shot.get("id")
            if not isinstance(sid, str) or not sid or sid in self.shots:
                self.errors.append("shot IDs must be unique nonempty strings")
                continue
            self.shots[sid] = shot
            span = self.interval(shot.get("frames"), f"shot {sid}")
            if span:
                spans[sid] = span
                if span[1] > total:
                    self.errors.append(f"shot {sid}: extends beyond film")
            self.require(shot.get("clothing_purpose"), f"shot {sid}: visible clothing purpose missing")
            self.require(shot.get("look_ids"), f"shot {sid}: no looks")
            for lid in shot.get("look_ids", []):
                if lid not in self.looks:
                    self.errors.append(f"shot {sid}: unknown look {lid}")
            reads[sid] = []
            self.require(shot.get("clear_read_intervals"), f"shot {sid}: no clear clothing read interval")
            for value in shot.get("clear_read_intervals", []):
                read = self.interval(value, f"shot {sid} clear read")
                if read and span:
                    reads[sid].append(read)
                    if read[0] < span[0] or read[1] > span[1]:
                        self.errors.append(f"shot {sid}: clear read outside shot")
            previous = None
            for read in sorted(reads[sid]):
                if previous and read[0] < previous[1]:
                    self.errors.append(f"shot {sid}: clear-read intervals overlap")
                previous = read
            checks = [("storyboard_asset_id", {"storyboard"}, "storyboard")]
            needs_previs = (shot.get("space_mode") == "shared_world" or shot.get("previs_required") is True or
                            self.p.get("presentation", {}).get("recipe_id") == "continuous_route")
            if needs_previs or shot.get("previs_asset_id"):
                checks.append(("previs_asset_id", {"previs"}, "previs"))
            for field, kind, scope in checks:
                aid = shot.get(field)
                self.asset_ref(aid, f"shot {sid} {field}", kind)
                self.approval(aid, scope)
            execution = shot.get("execution_mode", "generate")
            if execution not in {"generate", "reuse_clip"}:
                self.errors.append(f"shot {sid}: execution_mode must be generate or reuse_clip")
            if execution == "reuse_clip":
                self.inspect_clip_inputs(shot, span, fps)
            inputs = shot.get("input_asset_ids", [])
            if execution == "generate":
                self.require(inputs, f"shot {sid}: no planned source image input")
            for aid in inputs:
                asset = self.asset_ref(aid, f"shot {sid} input", {"still", "frame_extract"})
                if asset:
                    if asset.get("kind") == "still":
                        # Genuine prior still approval can be reused; never request it again just for this schema.
                        self.approval(aid, "still")
                    else:
                        self.inspect_frame_reuse(aid, asset)
            for aid in shot.get("scene_reference_asset_ids", []):
                self.asset_ref(aid, f"shot {sid} scene", {"scene", "still"})
            if shot.get("space_mode", "independent") not in {"independent", "shared_world"}:
                self.errors.append(f"shot {sid}: invalid space_mode")
        intervals = sorted(spans.items(), key=lambda x: (x[1][0], x[1][1]))
        expected = {}
        for i, (sid, (start, end)) in enumerate(intervals):
            if i == 0 and start != 0:
                self.errors.append("timeline must start at frame 0")
            if i:
                prev, (pstart, pend) = intervals[i-1]
                if start > pend:
                    self.errors.append(f"timeline gap before {sid}")
                if start <= pstart or end <= pend:
                    self.errors.append("shots must advance in time; use a single composited shot for parallel panels")
                expected[(prev, sid)] = (start, pend)  # A hard cut is [n,n).
        if intervals and max(v[1] for _, v in intervals) != total:
            self.errors.append("timeline end does not equal frame_count")
        points = sorted({x for span in spans.values() for x in span})
        for a, b in zip(points, points[1:]):
            if sum(s <= a < e for s, e in spans.values()) > 2:
                self.errors.append(f"three-way or greater overlap at [{a},{b})")
        found = {}
        overlap = 0
        for tr in self.records(self.p, "transitions"):
            pair = (tr.get("from_shot"), tr.get("to_shot"))
            value = self.interval(tr.get("frames"), f"transition {pair}", allow_zero=True)
            if pair in found:
                self.errors.append(f"duplicate transition {pair}")
            found[pair] = value
            if pair not in expected or value != expected[pair]:
                self.errors.append(f"transition {pair}: interval must exactly equal neighboring shot overlap")
            if value:
                length = value[1] - value[0]
                overlap += length
                if tr.get("overlap_frames") != length:
                    self.errors.append(f"transition {pair}: overlap_frames mismatch")
                if not tr.get("method"):
                    self.missing.append(f"transition {pair}: method missing")
                for sid in pair:
                    for a, b in reads.get(sid, []):
                        if a < value[1] and value[0] < b:
                            self.errors.append(f"shot {sid}: clear clothing read intersects transition")
        for pair in expected:
            if pair not in found:
                self.errors.append(f"missing transition record {pair}")
        if intervals and sum(e-s for s, e in spans.values()) - overlap != total:
            self.errors.append("sum of shot lengths minus overlap does not equal film frame_count")
        self.timeline = {"frame_count": total, "overlap_frames": overlap,
                         "clear_read_frames_by_shot": {sid: sum(b-a for a,b in v) for sid,v in reads.items()}}

    def inspect_space(self):
        routed = [s for s in self.shots.values() if s.get("space_mode") == "shared_world"]
        if self.p.get("presentation", {}).get("recipe_id") == "continuous_route" and not routed:
            self.missing.append("continuous_route requires shared_world shots")
        if not routed:
            return
        space = self.p.get("space")
        if not isinstance(space, dict):
            self.missing.append("shared_world requires common space data")
            return
        self.require(space.get("id"), "space ID missing")
        if space.get("units") not in {"metres", "schematic"} or space.get("axes") != "x_right_y_up_z_forward":
            self.errors.append("shared space requires metres/schematic and x_right_y_up_z_forward")
        if space.get("units") == "schematic":
            self.require(space.get("unit_note"), "schematic space requires a note that physical scale is unmeasured")
        geometry = self.records(space, "geometry")
        self.require(geometry, "shared space geometry missing")
        landmarks = set()
        for item in geometry:
            gid = item.get("id")
            if not isinstance(gid, str) or not gid or gid in landmarks:
                self.errors.append("geometry IDs must be unique nonempty strings")
                continue
            landmarks.add(gid)
            points = item.get("vertices")
            if not isinstance(points, list) or not points or not all(vector(p) for p in points):
                self.errors.append(f"geometry {gid}: vertices must contain 3D coordinates")
        common = self.p.get("shared_space_asset_id")
        self.asset_ref(common, "shared space source", {"space_plan"})
        path = self.files.get(common)
        if path:
            try:
                if json.loads(path.read_text(encoding="utf-8-sig")) != space:
                    self.errors.append("shared-space source JSON differs from current plan.space; rebuild both views")
            except (ValueError, OSError):
                self.errors.append("shared-space source is not readable JSON")
        routes = self.records(space, "routes")
        byid = {r.get("shot_id"): r for r in routes}
        if len(byid) != len(routes):
            self.errors.append("duplicate shared-space route shot_id")
        for shot in routed:
            sid = shot["id"]
            for field, kinds in (("overhead_asset_id", {"overhead"}), ("previs_asset_id", {"previs"})):
                aid = shot.get(field)
                asset = self.asset_ref(aid, f"route {sid} {field}", kinds)
                if asset:
                    parent = asset.get("derived_from", {})
                    if (parent.get("asset_id") != common or not self.hashes.get(common) or
                            parent.get("sha256") != self.hashes.get(common)):
                        self.missing.append(f"{aid}: exact shared-space provenance missing/stale")
                    if field == "overhead_asset_id":
                        self.approval(aid, "overhead")
            route = byid.get(sid)
            if not route:
                self.missing.append(f"route {sid}: trajectory/projection data missing")
                continue
            time_sets = []
            for key in ("character_samples", "camera_samples", "projected_samples"):
                samples = self.records(route, key)
                frames = [s.get("frame") for s in samples]
                if len(frames) < 3 or not all(integer(f) for f in frames) or frames != sorted(set(frames)):
                    self.errors.append(f"route {sid} {key}: need at least three strictly increasing integer control frames")
                    continue
                time_sets.append(frames)
                if [frames[0], frames[-1]] != shot.get("frames"):
                    self.errors.append(f"route {sid} {key}: endpoint times must equal shot boundaries")
                for sample in samples:
                    if key == "character_samples":
                        if not vector(sample.get("position")) or not number(sample.get("heading_degrees")):
                            self.errors.append(f"route {sid}: invalid character position/heading")
                        self.require(sample.get("gait_phase"), f"route {sid}: gait phase missing")
                    elif key == "camera_samples":
                        pos, target = sample.get("position"), sample.get("target")
                        fov = sample.get("vertical_fov_degrees")
                        if not vector(pos) or not vector(target) or pos == target or not number(fov) or not 1 < fov < 179:
                            self.errors.append(f"route {sid}: invalid camera position/target/FOV")
                    else:
                        height = sample.get("person_height_fraction")
                        if not vector(sample.get("person_center_uv"), 2) or not number(height) or height <= 0:
                            self.errors.append(f"route {sid}: invalid projected person size/position")
                        self.require(sample.get("visible_clothing"), f"route {sid}: projection lacks visible clothing")
                        if any(g not in landmarks for g in sample.get("visible_landmark_ids", [])):
                            self.errors.append(f"route {sid}: projected sample names unknown landmark")
            if len(time_sets) == 3 and not (time_sets[0] == time_sets[1] == time_sets[2]):
                self.errors.append(f"route {sid}: character/camera/projection control times must match")
            if route.get("character_samples") == route.get("camera_samples"):
                self.errors.append(f"route {sid}: separate character/camera trajectories required")

    def run(self):
        if self.p.get("schema_version") != 1:
            self.errors.append("unsupported schema_version")
        for key in ("editorial", "presentation", "weeks", "film"):
            if not isinstance(self.p.get(key), dict):
                self.errors.append(f"{key} must be an object")
                self.p[key] = {}
        self.inspect_assets()
        self.inspect_editorial()
        self.inspect_timeline()
        self.inspect_space()
        self.errors = list(dict.fromkeys(self.errors))
        self.missing = list(dict.fromkeys(self.missing))
        ready = not self.errors and not self.missing
        return {"status": "invalid" if self.errors else "complete_evidence" if ready else "incomplete",
                "ready_for_generation": ready, "errors": self.errors, "incomplete": self.missing,
                "warnings": self.warnings, "timeline": self.timeline,
                "limits": "Checks structure, local files, hashes and recorded approval fields only. Does not authenticate receipts, inspect images/video, solve projection/collisions, verify visual comfort, or certify Grok execution."}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("output", type=Path)
    init.add_argument("--recipe", choices=sorted(RECIPES), default="sequential_lookbook")
    init.add_argument("--path-base", choices=("plan", "project"), default="plan")
    check = sub.add_parser("validate")
    check.add_argument("plan", type=Path)
    check.add_argument("--project-root", type=Path)
    check.add_argument("--for-generation", action="store_true")
    args = parser.parse_args()
    if args.command == "init":
        template = Path(__file__).resolve().parent.parent / "assets" / "production_plan.template.json"
        p = json.loads(template.read_text(encoding="utf-8-sig"))
        p["presentation"]["recipe_id"] = args.recipe
        p["presentation"]["layout_id"] = ("parallel_comparison" if args.recipe == "parallel_comparison"
                                          else "primary_detail" if args.recipe == "primary_detail_experiment"
                                          else "single_sequential")
        p["path_base"] = args.path_base
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as out:
            json.dump(p, out, ensure_ascii=False, indent=2)
            out.write("\n")
        print(f"Created draft: {args.output}")
        return 0
    try:
        p = json.loads(args.plan.read_text(encoding="utf-8-sig"))
        if not isinstance(p, dict):
            raise ValueError("plan root must be an object")
        result = Check(p, args.plan, args.project_root).run()
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({"status": "invalid", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["errors"] else 3 if args.for_generation and result["incomplete"] else 0


if __name__ == "__main__":
    sys.exit(main())
