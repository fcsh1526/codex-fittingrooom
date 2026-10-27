"""New-only deterministic F04 geometry audit; no AI, source edits or movie.

Read accepted route/camera helpers, freeze six world-space road rectangles,
and project exactly that geometry at101 F04 positions. This intentionally
reveals, rather than silently fixes, the approved-mid direction conflict.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[2]
SOURCE = PILOT / "accepted_keys_previs_2026-10-16/build_previs.py"
spec = importlib.util.spec_from_file_location("f04_readonly_accepted_camera", SOURCE)
previs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previs)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, text):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(text)


def project(point, frame, width=360, height=640):
    x, y, z = point
    cx, cz = frame["camera"]
    fx, fz = frame["forward"]
    dep = (x - cx) * fx + (z - cz) * fz
    if dep <= .16:
        return None
    return [width * .5 + ((x - cx) * fz - (z - cz) * fx) * height * frame["focal"] / dep,
            height * .42 - (y - 1.30) * height * frame["focal"] / dep]


def main():
    sources = [SOURCE, PILOT / "accepted_keys_previs_2026-10-16/previs_plan.json",
               PILOT / "static_key_views_2026-10-16/build_key_views.py",
               PILOT / "continuous_route_storyboard_2026-10-16/render_route.py",
               PILOT / "continuous_route_storyboard_2026-10-16/route_plan.json"]
    before = {str(p): digest(p) for p in sources}
    stripes = [{"id": "C" + str(i + 1), "points": [[11.35, 0, z], [13.7, 0, z],
                [13.7, 0, z + .23], [11.35, 0, z + .23]]}
               for i, z in enumerate([2.65 + .46 * j for j in range(6)])]
    frames = []
    for percentage in range(101):
        t = 11.25 + 4.5 * percentage / 100
        p, c, aim, focal = previs.camera_values(t)
        forward = (aim - c) / previs.np.linalg.norm(aim - c)
        heading = previs.site.position(t + .03) - previs.site.position(t - .03)
        heading /= previs.np.linalg.norm(heading)
        frame = {"percentage": percentage, "source_t": t, "person": p.tolist(), "camera": c.tolist(),
                 "forward": forward.tolist(), "heading": heading.tolist(), "focal": float(focal)}
        a, b = [project(v, frame) for v in stripes[2]["points"][:2]]
        frame["white_long_axis_angle_from_horizontal_deg"] = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) if a and b else None
        frames.append(frame)
    data = {"stripes": stripes, "frames": frames, "road_z": [2.5, 5.4],
            "company_z": 8.8, "company_x": [-6, 20], "door_x": [11.7, 13.3],
            "eye_height": 1.30, "horizon": .42,
            "fixed_world_geometry": True, "coordinate_units": "schematic relative units; not surveyed"}
    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    template = (HERE / "f04-fixed-crosswalk.template.html").read_text(encoding="utf-8")
    assert template.count("__MODEL_DATA__") == 1
    output = template.replace("__MODEL_DATA__", compact)
    assert len(output.encode("utf-8")) < 1024 * 1024
    write_new(HERE / "f04-fixed-crosswalk.html", output)
    write_new(HERE / "geometry_plan.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    # Static SVG uses the same frozen vertices and projection, never manually
    # turns the paint. Labels are planning annotations, not Reel overlays.
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="760" viewBox="0 0 1120 760" style="color:CanvasText;background:Canvas">',
             '<title>F04 fixed six-stripe projection: accepted original camera</title>',
             '<rect width="1120" height="760" fill="Canvas"/>',
             '<defs><clipPath id="panel"><rect width="340" height="604"/></clipPath></defs>']
    for n, index in enumerate([0, 50, 100]):
        frame = frames[index]
        tx = 20 + n * 370
        parts.append(f'<g transform="translate({tx},40)"><text x="0" y="-15" fill="currentColor" font-size="18">{["Start","Mid","End"][n]} — {frame["white_long_axis_angle_from_horizontal_deg"]:.1f}° from horizontal</text>')
        parts.append('<rect width="340" height="604" fill="Canvas" stroke="currentColor" opacity=".2"/>')
        parts.append('<g clip-path="url(#panel)">')
        for stripe in stripes:
            points = [project(v, frame, 340, 604) for v in stripe["points"]]
            if all(p is not None for p in points):
                points_text = " ".join(f'{p[0]:.2f},{p[1]:.2f}' for p in points)
                parts.append(f'<polygon points="{points_text}" fill="GrayText" fill-opacity=".3" stroke="currentColor" stroke-width="1"/>')
        for z in [2.5, 5.4]:
            a, b = [project(v, frame, 340, 604) for v in [(8, 0, z), (18, 0, z)]]
            if a and b:
                parts.append(f'<path d="M{a[0]:.2f},{a[1]:.2f}L{b[0]:.2f},{b[1]:.2f}" fill="none" stroke="currentColor"/>')
        feet = project([frame['person'][0], 0, frame['person'][1]], frame, 340, 604)
        top = project([frame['person'][0], 1.68, frame['person'][1]], frame, 340, 604)
        if feet and top:
            parts.append(f'<path d="M{top[0]:.2f},{top[1]+15:.2f}L{feet[0]:.2f},{feet[1]-40:.2f}m0,-70l-22,70m22,-70l22,70" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="{top[0]:.2f}" cy="{top[1]+7:.2f}" r="9" fill="currentColor"/>')
        parts.append('</g></g>')
    parts.append('<text x="20" y="710" fill="currentColor" font-size="18">Same six rectangles. Original mid projects almost horizontally, unlike approved mid vertical/depth direction.</text></svg>')
    write_new(HERE / "f04-fixed-crosswalk-three-views.svg", "\n".join(parts))
    for path in sources:
        assert digest(path) == before[str(path)], path
    receipt = {"status": "deterministic_F04_geometry_audit_pending_editorial_camera_decision",
               "source_files_unchanged": before, "shared_world_stripe_count": 6,
               "all_frames_share_identical_stripe_vertices": True,
               "original_F04_previs_time_interval": [11.25, 15.75],
               "start_mid_end_axis_angles_deg": [frames[i]["white_long_axis_angle_from_horizontal_deg"] for i in [0, 50, 100]],
               "approved_mid_direction_matched": False,
               "limits": ["Original schematic camera/geometry preserved, not photoreal image calibration.",
                          "Original-mid white long axis is about14degrees from horizontal; approved mid asks depth/near-vertical stripes.",
                          "Do not rotate paint independently per frame. A later camera or one global stripe orientation decision is required.",
                          "This is not a new film, exact source-frame match, identity approval or generator feasibility proof."],
               "AI_calls": 0, "Grok_calls": 0,
               "output_files": {p.name: {"sha256": digest(p), "bytes": p.stat().st_size} for p in [HERE / "f04-fixed-crosswalk.html", HERE / "geometry_plan.json", HERE / "f04-fixed-crosswalk-three-views.svg"]}}
    write_new(HERE / "geometry_preview_receipt.json", json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"html": str(HERE / "f04-fixed-crosswalk.html"), "mid_original_angle_deg": frames[50]["white_long_axis_angle_from_horizontal_deg"], "approved_mid_direction_matched": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
