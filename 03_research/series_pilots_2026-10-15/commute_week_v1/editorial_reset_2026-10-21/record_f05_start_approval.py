from pathlib import Path
import json

base = Path(__file__).resolve().parent
start = base / 'F05_full_start_01'
question = '第五套新起始圖的臉、白襯衫／黑A字裙、鈷藍包、黑鞋與抬腳姿勢是否可以沿用？裙面保留原參照細紋，鞋位與背景細節略有變化。依你訂的新圖核准流程，確認後才做後段圖與影片。'
receipt = {
    'date': '2026-10-21',
    'question_item_id': '["request_user_input_async","call_f0e6c171c45d4182a7c53c2c1edcf3fd",0]',
    'asset': 'F05_M03_L04_full_start_candidate_A.png',
    'sha256': 'ac588ec1674df43923140e17f46c4734706cf834f2b7f5599aeeec60376f9c82',
    'question': question, 'answer': '可以，沿用這張',
    'status': 'user_visual_approved_exact_still',
    'scope': 'Exact F05 full-person first still, including disclosed skirt texture and regenerated shoe/background differences; allows preparation of a compatible late candidate, which needs separate user visual approval before video.',
    'F05_motion_approval': False, 'complete_film_approval': False,
    'publishing_approval': False,
}
(start / 'user_still_approval.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
review_path = start / 'user_review_request.json'
review = json.loads(review_path.read_text(encoding='utf-8-sig'))
review.update(answer=receipt['answer'], status=receipt['status'], approval_receipt='user_still_approval.json')
review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
gen_path = start / 'generation_receipt.json'
gen = json.loads(gen_path.read_text(encoding='utf-8-sig'))
gen.update(status=receipt['status'], approval_receipt='user_still_approval.json', next='Prepare one compatible full-outfit late candidate on same visible facade walkway; separate new-still approval before Grok motion. No hard jump to old doorway.')
gen_path.write_text(json.dumps(gen, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'approval_saved': str(start / 'user_still_approval.json'), 'status': receipt['status']}, ensure_ascii=False))
