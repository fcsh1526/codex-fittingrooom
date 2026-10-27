from pathlib import Path
import copy,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=read(HERE/'google_drive_delivery_2026-10-22.json')
manifest=read(HERE/'local_manifest.json')
manifest.update(status=receipt['status'],editorial_content_week='2026-W43',video_drive=receipt['video'],caption_doc=receipt['caption_doc'],delivery_receipt=str((HERE/'google_drive_delivery_2026-10-22.json').relative_to(ROOT)))
write(HERE/'local_manifest.json',manifest)

registry_path=ROOT/'04_prompts/material_pool/series_registry.json'
registry=read(registry_path)
old_other=[copy.deepcopy(s) for s in registry['series'] if s['series_id']!='SERIES_COMMUTE_WEEK']
series=next(s for s in registry['series'] if s['series_id']=='SERIES_COMMUTE_WEEK')
record_keys=['status','adopted_date','latest_proposal_status','complete_five_look_film_approval','latest_source_plan','latest_film_preview','latest_feedback_path','root_cause_status','current_remaining_expansion_authorized']
old_state={k:copy.deepcopy(series.get(k)) for k in record_keys}
series.setdefault('state_history',[]).append({'archived_on':'2026-10-22','previous_registry_updated_date':registry['updated_date'],'reason':'Preserve previous urban_v3 rejected-state evidence before recording newly approved continuous-route film','state':old_state})
base='03_research/series_pilots_2026-10-15/commute_week_v1/editorial_reset_2026-10-21/pace_rebuild_2026-10-22/'
series.update({
 'status':'publication_approved_trial_further_refinement_required',
 'adopted_date':'2026-10-22',
 'latest_proposal_status':'initial_editing_subtype_accepted_curve_camera_and_ghosting_refinement_pending',
 'complete_five_look_film_approval':base+'context_review_v2/user_publication_approval_2026-10-22.json',
 'latest_source_plan':base+'context_review_v2/build_manifest.json',
 'latest_feedback_path':base+'context_review_v2/user_publication_approval_2026-10-22.json',
 'root_cause_status':'cadence_partial_improvement_accepted_curved_camera_unachieved_ghosting_discomfort_remains',
 'current_remaining_expansion_authorized':False,
 'editing_subtype':'同一路線・連續行進換裝',
 'editing_type_record':base+'TYPE_AND_NEXT_VERSION.md',
 'accepted_recipe':base+'ACCEPTED_RECIPE.md',
 'current_film_usage_ledger_id':None,
 'source_usage_trace_note':'Existing material-pool usage IDs retained as historical trace. Current five source clips and selected intervals are recorded in latest_source_plan; no invented new consumption record.',
 'next_reviewable_artifact':'Shared-space overhead drawing with separate camera/character curves and synchronized camera-view previs, before new photography or footage.',
 'latest_film_preview':{
  'status':'publication_approved_initial_version_refinement_pending',
  'file':base+'context_review_v2/review.mp4','sha256':'e5e8a90878b00bab29ecf4da32a6fe5472e1376f1b835b999beaa9a812e225c2',
  'frames':511,'seconds':511/24,'pixels':[720,1280],'fps':24,
  'native_speed':True,'baked_text':False,'audio':False,
  'user_film_approval':base+'context_review_v2/user_publication_approval_2026-10-22.json',
  'publishable':True,'actually_published':False,'instagram_url':None,
  'full_continuous_playback_user_self_report':None,'assistant_continuous_visual_playback':False,
  'exact_world_or_camera_path_verified':False,'ghosting_comfort_resolved':False,'zero_sliding_verified':False,
  'residual_user_requests':['brisker native walking','camera and character follow distinct coordinated curves','reduce uncomfortable ghosting flicker'],
  'drive_delivery_receipt':str((HERE/'google_drive_delivery_2026-10-22.json').relative_to(ROOT)),
  'drive_video':receipt['video']['url'],'caption_document':receipt['caption_doc']['url']
 }
})
registry['updated_date']='2026-10-22'
assert [s for s in registry['series'] if s['series_id']!='SERIES_COMMUTE_WEEK']==old_other
assert series['state_history'][-1]['state']['latest_film_preview']==old_state['latest_film_preview']
write(registry_path,registry)

archive_path=ROOT/'10_automation/google_drive_archive_registry.json'
archive=read(archive_path)
assert '2026-W43' not in archive['weeks']
archive['updated_date']='2026-10-22'
archive['series_reuse_policy']='A new edited series uses its editorial content batch week; source material pool weeks are recorded separately. The approved five-look commute series is W43 editorial content reusing W41 clothing material, not a claim of fresh W43 trend research.'
archive['weeks']['2026-W43']={
 'id':receipt['drive_folder']['id'],'name':'2026-W43','parent_id':receipt['drive_root']['id'],
 'path':'800.Codex IG/2026-W43','url':receipt['drive_folder']['url'],
 'content':'One user-approved continuous-route five-look commute Reel and native Google Docs caption/handoff.',
 'source_material_pool_weeks':['2026-W41'],
 'publication_status':'ready_not_posted',
 'delivery_receipt':str((HERE/'google_drive_delivery_2026-10-22.json').relative_to(ROOT))
}
write(archive_path,archive)
print('Updated delivery manifest, commute series current state with preserved prior state, and verified W43 archive mapping.')
