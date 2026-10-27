"""New F04 camera-only proposal over the existing fixed crossing and route.

Keeps original camera+aim+framing at start. Camera offset moves continuously
to world+x side at mid and a little behind at end; paint vertices never change.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("f04_fixed_geometry", HERE / "build_geometry_preview.py")
fixed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixed)


def mix(a, b, u):
    return [a[i] + (b[i] - a[i]) * u for i in range(len(a))]


def hermite(a, b, va, vb, u, interval=.5):
    return [(2*u**3-3*u*u+1)*a[i]+(u**3-2*u*u+u)*interval*va[i]
            +(-2*u**3+3*u*u)*b[i]+(u**3-u*u)*interval*vb[i] for i in range(2)]


def clip_screen(points, width=360, height=640):
    out = points
    for axis, boundary, sign in [(0, 0, 1), (0, width, -1), (1, 0, 1), (1, height, -1)]:
        source, out = out, []
        for i, b in enumerate(source):
            a = source[i-1]
            da, db = sign*(a[axis]-boundary), sign*(b[axis]-boundary)
            if (da >= 0) != (db >= 0):
                t = da/(da-db)
                out.append([a[k]+(b[k]-a[k])*t for k in range(2)])
            if db >= 0:
                out.append(b)
    return out


def main():
    source = HERE / "geometry_plan.json"
    template_path = HERE / "f04-fixed-crosswalk.template.html"
    protection = {str(p): fixed.digest(p) for p in [source, template_path, HERE / "f04-fixed-crosswalk.html", HERE / "geometry_preview_receipt.json"]}
    original = json.loads(source.read_text(encoding="utf-8"))
    data = json.loads(json.dumps(original))
    first = original["frames"][0]
    p0, c0 = first["person"], first["camera"]
    o0 = [c0[i]-p0[i] for i in range(2)]
    o1, o2 = [4.0, 0.0], [4.0, -1.3]
    v0 = [(o1[i]-o0[i])/.5 for i in range(2)]
    v1, v2 = [0.0, 0.0], [0.0, -2.6]
    original_aim_offset = [first["forward"][i] * math.dist(c0,p0) + c0[i]-p0[i] for i in range(2)]
    # Recover the actual original look target rather than assuming its distance.
    _, _, original_aim, _ = fixed.previs.camera_values(11.25)
    original_aim_offset = [float(original_aim[i])-p0[i] for i in range(2)]
    checks = []
    for index, frame in enumerate(data["frames"]):
        u = index/100
        offset = hermite(o0,o1,v0,v1,u*2) if u <= .5 else hermite(o1,o2,v1,v2,(u-.5)*2)
        frame["camera"] = [frame["person"][i]+offset[i] for i in range(2)]
        s = min(1.0,u*2); smooth=s*s*(3-2*s)
        aim_offset = [v*(1-smooth) for v in original_aim_offset]
        aim = [frame["person"][i]+aim_offset[i] for i in range(2)]
        direction = [aim[i]-frame["camera"][i] for i in range(2)]
        length=math.hypot(*direction)
        frame["forward"]=[v/length for v in direction]
        frame["focal"] = first["focal"] + (1.45-first["focal"])*smooth
        if u > .5:
            end_u=(u-.5)*2; end_smooth=end_u*end_u*(3-2*end_u)
            frame["focal"]=1.45+(1.15-1.45)*end_smooth
        frame["camera_offset_from_person"] = offset
        frame["aim"] = aim
        a,b=[fixed.project(p,frame) for p in data["stripes"][2]["points"][:2]]
        angle=math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
        frame["white_long_axis_angle_from_horizontal_deg"]=angle
        frame["white_long_axis_deviation_from_vertical_deg"]=abs(90-abs(angle))
        top=fixed.project([frame['person'][0],1.70,frame['person'][1]],frame)
        feet=fixed.project([frame['person'][0],0,frame['person'][1]],frame)
        visible=[]
        for stripe in data["stripes"]:
            points=[fixed.project(p,frame) for p in stripe["points"]]
            if all(p is not None for p in points) and len(clip_screen(points))>=3:
                visible.append(stripe["id"])
        checks.append({"percentage":index,"head_top":top,"feet":feet,"visible_stripes":visible})
        assert offset[0]>0, "Camera cannot cross the person's opposite world-x side"
        assert top and feet and 0<top[0]<360 and 0<feet[0]<360 and 0<top[1]<feet[1]<640
        assert visible, f"No paint visible at{index}%"
    assert data["stripes"]==original["stripes"]
    assert all(f['person']==o['person'] and f['heading']==o['heading'] for f,o in zip(data['frames'],original['frames']))
    assert data['frames'][0]['camera']==first['camera']
    data["stage"]="new_camera_only_proposal_pending_user_review"
    template=template_path.read_text(encoding="utf-8")
    template=template.replace('mira-f04-fixed-crosswalk-20261020','mira-f04-camera-proposal-20261020').replace('mira-f04-progress','mira-f04-proposal-progress')
    template=template.replace('第四段：同一組白線，鏡頭持續移動','第四段提案：側面過街，再跟到公司側')
    template=template.replace('由同一地面六條固定白線與原分鏡相機計算的透視圖','同一地面六條固定白線與修正相機路徑的透視提案')
    template=template.replace('原分鏡中景：白條接近橫向；與核准中景的朝遠處方向不同。','鏡位修正提案：中景白條朝景深延伸；尚待確認。')
    template=template.replace('固定6條白線；只有人物與相機沿原路徑移動。','固定6條白線、同一人物路線；這是新的鏡位提案。')
    output=template.replace('__MODEL_DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')))
    fixed.write_new(HERE/'geometry-proposal.html',output)
    fixed.write_new(HERE/'geometry-proposal-plan.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="760" viewBox="0 0 1120 760" style="color:CanvasText;background:Canvas">',
           '<title>F04 proposed camera, same fixed crossing</title><rect width="1120" height="760" fill="Canvas"/>',
           '<defs><clipPath id="proposal-panel"><rect width="340" height="604"/></clipPath></defs>']
    for n,index in enumerate([0,50,100]):
        frame=data['frames'][index]; tx=20+n*370
        parts.append(f'<g transform="translate({tx},40)"><text x="0" y="-15" fill="currentColor" font-size="18">{["Start","Mid","End"][n]} — camera proposal</text><g clip-path="url(#proposal-panel)"><rect width="340" height="604" fill="Canvas" stroke="currentColor" opacity=".2"/>')
        for stripe in data['stripes']:
            points=[fixed.project(p,frame,340,604) for p in stripe['points']]
            if all(p is not None for p in points):
                pp=' '.join(f'{p[0]:.2f},{p[1]:.2f}' for p in points)
                parts.append(f'<polygon points="{pp}" fill="GrayText" fill-opacity=".3" stroke="currentColor"/>')
        for z in data['road_z']:
            a,b=[fixed.project(p,frame,340,604) for p in [(8,0,z),(18,0,z)]]
            if a and b:parts.append(f'<path d="M{a[0]:.2f},{a[1]:.2f}L{b[0]:.2f},{b[1]:.2f}" fill="none" stroke="currentColor"/>')
        feet=fixed.project([frame['person'][0],0,frame['person'][1]],frame,340,604)
        top=fixed.project([frame['person'][0],1.7,frame['person'][1]],frame,340,604)
        parts.append(f'<path d="M{top[0]:.2f},{top[1]+15:.2f}L{feet[0]:.2f},{feet[1]-40:.2f}m0,-70l-22,70m22,-70l22,70" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="{top[0]:.2f}" cy="{top[1]+7:.2f}" r="9" fill="currentColor"/></g></g>')
    parts.append('<text x="20" y="710" fill="currentColor" font-size="18">Same six world rectangles; camera moves to side, then slightly behind. New proposal, not an image match.</text></svg>')
    fixed.write_new(HERE/'geometry-proposal-three-views.svg','\n'.join(parts))
    for path,sha in protection.items():assert fixed.digest(Path(path))==sha
    receipt={"stage":"new_camera_only_proposal_pending_user_approval","AI_calls":0,"Grok_calls":0,
             "old_files_unchanged":protection,"same_world_stripe_vertices":True,"same_person_route":True,
             "camera_start_preserved":True,"start_camera_aim_and_focal_preserved":True,
             "camera_offset_knots":[o0,o1,o2],"camera_offset_derivatives":[v0,v1,v2],
             "new_mid_raw_angle_deg":data['frames'][50]['white_long_axis_angle_from_horizontal_deg'],
             "new_mid_deviation_from_vertical_deg":data['frames'][50]['white_long_axis_deviation_from_vertical_deg'],
             "old_mid_angle_from_horizontal_deg":original['frames'][50]['white_long_axis_angle_from_horizontal_deg'],
             "all101_head_top_and_feet_in_frame":True,"all101_camera_offset_x_positive":True,
             "start_mid_end_projection_checks":[checks[i] for i in [0,50,100]],
             "checks":checks,"focal_ratio_is_abstract_projection_not_physical_lens_metadata":True,
             "original_approved_photoreal_frames_matched":False,"user_camera_proposal_approval":None,
             "limits":["Fixed point/edge projection is not limb, sleeve, bag or all-contour framing QA.","No physical50mm lens metadata or generator reconstruction is demonstrated.","The same original path is retained; new camera motion is not the previously accepted camera curve except its first state.","No continuous playback, photoreal source alignment, finished-film or publication approval is inferred."],
             "output_files":{p.name:{"sha256":fixed.digest(p),"bytes":p.stat().st_size} for p in [HERE/'geometry-proposal.html',HERE/'geometry-proposal-plan.json',HERE/'geometry-proposal-three-views.svg']}}
    fixed.write_new(HERE/'geometry-proposal-receipt.json',json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['new_mid_raw_angle_deg','new_mid_deviation_from_vertical_deg','all101_head_top_and_feet_in_frame','start_mid_end_projection_checks']},ensure_ascii=False))


if __name__=='__main__':main()
