"""Build an additive, provenance-preserving material index; never modify source rows.

The independent series_registry.json is maintained by editors, not by this builder.
No network access, media generation, posting, scheduling or production quota here.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path


SCHEMA_VERSION = 1
GROUP_FIELDS = ('clothing_item', 'color_palette', 'fabric', 'fit', 'styling_rules')
REQUIRED_FIELDS = ('id', 'week', 'trend_name', *GROUP_FIELDS)


def iso_monday(week):
    match = re.fullmatch(r'(\d{4})-W(\d{2})', week)
    if not match:
        raise ValueError(f'Not a strict ISO week: {week!r}')
    return date.fromisocalendar(int(match[1]), int(match[2]), 1)


def iso_week(day):
    year, week, _ = day.isocalendar()
    return f'{year}-W{week:02d}'


def normalize(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split()).casefold()


def digest(value):
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def material_id(week, row_id):
    return 'mi_' + digest([week, row_id])[:20]


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def relative(root, path):
    return path.relative_to(root).as_posix()


def read_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        missing = set(REQUIRED_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'{path}: missing columns {sorted(missing)}')
        rows = []
        seen = {}
        for line, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f'{path}:{line}: malformed CSV row')
            if not row['id'].strip() or not row['week'].strip():
                raise ValueError(f'{path}:{line}: missing id/week')
            key = (row['week'], row['id'])
            if key in seen and seen[key] != row:
                raise ValueError(f'{path}:{line}: conflicting duplicate {key}')
            seen[key] = row
            rows.append((line, row))
    return rows


def editorial(row):
    return row.get('status', '').startswith('editorial_') or bool(
        re.search(r'-E\d+$', row['id']))


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def build(root, as_of, window_weeks=3):
    root = Path(root).resolve()
    as_of = date.fromisoformat(as_of) if isinstance(as_of, str) else as_of
    if not 1 <= window_weeks <= 12:
        raise ValueError('window_weeks must be between 1 and 12')
    output = root / '04_prompts/material_pool'
    index_path = output / 'material_index.json'
    registry_path = output / 'series_registry.json'
    previous = read_json(index_path) if index_path.exists() else {}
    if previous and previous.get('schema_version') != SCHEMA_VERSION:
        raise ValueError('Unsupported previous material index schema')
    if previous and previous['as_of'] > as_of.isoformat():
        raise ValueError('Refusing to backdate the persistent index; use a separate workspace for historical builds')
    registry = read_json(registry_path) if registry_path.exists() else {}
    if registry and registry.get('schema_version') != SCHEMA_VERSION:
        raise ValueError('Unsupported series registry schema')

    watched = {}

    def watch(path):
        watched[relative(root, path)] = file_hash(path)

    if registry_path.exists():
        watch(registry_path)
    master_path = root / '04_prompts/item_prompt_database.csv'
    watch(master_path)
    sources = []
    occurrences = defaultdict(list)
    quarantined = []

    def add(path, rows, role, expected_week=None, receipt_state=None):
        for line, row in rows:
            try:
                iso_monday(row['week'])
            except ValueError:
                if role == 'original_weekly_csv':
                    raise ValueError(f'{path}:{line}: invalid source week')
                quarantined.append({'path': relative(root, path), 'line': line,
                                    'reason': 'non_iso_or_test_week', 'row': row})
                continue
            if expected_week and row['week'] != expected_week:
                raise ValueError(f'{path}:{line}: row week differs from source folder')
            if role == 'original_weekly_csv' and (editorial(row) or any(
                    not row[field].strip() for field in REQUIRED_FIELDS)):
                raise ValueError(f'{path}:{line}: original source requires nonempty research fields')
            occurrence = {'path': relative(root, path), 'line': line, 'role': role,
                          'file_sha256': watched[relative(root, path)], 'row': row}
            if receipt_state is not None:
                occurrence['receipt_state'] = receipt_state
            occurrences[(row['week'], row['id'])].append(occurrence)

    add(master_path, read_rows(master_path), 'master_database')
    for path in sorted((root / '10_automation/runs').glob('*/source_perplexity.csv')):
        week = path.parent.name
        iso_monday(week)  # A misnamed source folder is an input error, not a usable import.
        watch(path)
        rows = read_rows(path)
        if not rows:
            raise ValueError(f'{path}: empty original source')
        receipt_path = path.parent / 'source_receipt.json'
        receipt_exists = receipt_path.exists()
        receipt = read_json(receipt_path) if receipt_exists else None
        state = 'missing'
        if receipt_exists:
            watch(receipt_path)
            receipt = receipt if isinstance(receipt, dict) else {}
            state = 'matched' if (receipt.get('sha256') == file_hash(path)
                and receipt.get('rows') == len(rows) and receipt.get('week') == week) else 'mismatch'
        sources.append({'week': week, 'path': relative(root, path),
                        'sha256': file_hash(path), 'rows': len(rows),
                        'receipt_path': relative(root, receipt_path) if receipt_exists else None,
                        'receipt_state': state,
                        'retrieved_date': receipt.get('retrieved_date') if receipt else None,
                        'report_url': receipt.get('report_url') if receipt else None,
                        'csv_url': receipt.get('csv_url') if receipt else None,
                        'external_claims_verified': False,
                        'evidence_limit': receipt.get('evidence_limit') if receipt else
                        'Saved CSV is available; retrieval receipt and external claim verification are absent.'})
        add(path, rows, 'original_weekly_csv', week, state)

    source_history = list(previous.get('source_history', []))
    source_snapshots = {digest(item['source']) for item in source_history}
    for source in sources:
        if digest(source) not in source_snapshots:
            source_history.append({'first_observed_as_of': as_of.isoformat(), 'source': source})
            source_snapshots.add(digest(source))

    def provenance_signature(items):
        # Row order and an unrelated row's change to the file hash do not make a new row revision.
        return sorted({(item['path'], item['role'], digest(item['row']), item.get('receipt_state', ''))
                       for item in items})

    old_entries = {entry['material_id']: entry for entry in previous.get('entries', [])}
    entries = []
    for (week, row_id), provenance in sorted(occurrences.items()):
        originals = [entry for entry in provenance if entry['role'] == 'original_weekly_csv']
        canonical = (originals or provenance)[0]['row']
        content_hash = digest(canonical)
        identity = material_id(week, row_id)
        old = old_entries.get(identity, {})
        revisions = list(old.get('revisions', []))
        if old and (old['content_sha256'] != content_hash or
                    provenance_signature(old['provenance']) != provenance_signature(provenance)):
            revisions.append({'observed_through': old['last_seen_as_of'],
                              'content_sha256': old['content_sha256'],
                              'row': old['row'], 'provenance': old['provenance'],
                              'conflicting_variants': old['conflicting_variants'],
                              'issues': old['issues']})
        variants = {}
        for occurrence in provenance:
            variants[digest(occurrence['row'])] = occurrence['row']
        conflict = len(variants) > 1
        origin = 'editorial_expansion' if editorial(canonical) else (
            'saved_weekly_source' if originals else 'legacy_source_unverified')
        issues = []
        if conflict:
            issues.append('conflicting_same_week_id')
        if any(item.get('receipt_state') == 'mismatch' for item in originals):
            issues.append('receipt_mismatch')
        if any(not canonical[field].strip() for field in REQUIRED_FIELDS):
            issues.append('incomplete_research_fields')
        group_id = 'mg_' + digest([normalize(canonical[field]) for field in GROUP_FIELDS])[:20]
        entry = {'material_id': identity, 'source_week': week, 'source_row_id': row_id,
                 'origin': origin, 'row': canonical, 'content_sha256': content_hash,
                 'group_id': group_id, 'external_claims_verified': False,
                 'first_seen_as_of': old.get('first_seen_as_of', as_of.isoformat()),
                 'last_seen_as_of': as_of.isoformat(), 'availability': 'present',
                 'issues': issues, 'provenance': provenance, 'revisions': revisions,
                 'conflicting_variants': list(variants.values()) if conflict else [],
                 'editor_notes': old.get('editor_notes', {})}
        entries.append(entry)
    # Removal from an input is visible; it never silently erases historical material.
    present_ids = {entry['material_id'] for entry in entries}
    for identity, old in old_entries.items():
        if identity not in present_ids:
            entries.append(dict(old, availability='absent_from_current_inputs'))
    entries.sort(key=lambda item: (item['source_week'], item['source_row_id']))

    groups = defaultdict(list)
    for entry in entries:
        groups[entry['group_id']].append(entry)
    group_records = []
    for identity, members in sorted(groups.items()):
        group_records.append({'group_id': identity,
            'comparison_only': True, 'fields': {key: members[0]['row'][key] for key in GROUP_FIELDS},
            'material_ids': [member['material_id'] for member in members],
            'source_weeks': sorted({member['source_week'] for member in members}),
            'trend_names': sorted({member['row']['trend_name'] for member in members}),
            'occasions': sorted({member['row'].get('occasion', '') for member in members}),
            'origins': sorted({member['origin'] for member in members})})

    plans = []
    for path in sorted((root / '10_automation/runs').glob('*/weekly_look_plan.csv')):
        watch(path)
        with path.open(encoding='utf-8-sig', newline='') as stream:
            looks = list(csv.DictReader(stream))
        plans.append({'path': relative(root, path), 'sha256': file_hash(path),
                      'source_week_label': path.parent.name,
                      'interpretation': 'Editorial plan only; status is not still or film approval.',
                      'looks': [{key: row.get(key) for key in
                                 ('look_id', 'model_profile_id', 'look_name', 'status')}
                                for row in looks]})

    monday = as_of - timedelta(days=as_of.isoweekday() - 1)
    weeks = [iso_week(monday - timedelta(weeks=offset))
             for offset in reversed(range(window_weeks))]
    current = [entry for entry in entries if entry['source_week'] in weeks
               and entry['availability'] == 'present']
    usable = [entry for entry in current if not entry['issues']]
    raw = [entry for entry in usable if entry['origin'] == 'saved_weekly_source']
    legacy = [entry for entry in usable if entry['origin'] == 'legacy_source_unverified']
    edits = [entry for entry in usable if entry['origin'] == 'editorial_expansion']
    source_by_week = {item['week']: item for item in sources}
    coverage = [{'week': week,
                 'saved_source_rows': source_by_week.get(week, {}).get('rows', 0),
                 'receipt_state': source_by_week.get(week, {}).get('receipt_state'),
                 'status': 'missing_original_csv' if week not in source_by_week else
                 ('needs_receipt_reconciliation' if source_by_week[week]['receipt_state'] == 'mismatch'
                  else 'saved_source_available_for_review')}
                for week in weeks]
    index = {'schema_version': SCHEMA_VERSION, 'as_of': as_of.isoformat(),
             'input_hashes': watched, 'sources': sources, 'source_history': source_history, 'entries': entries,
             'comparison_groups': group_records, 'quarantined_rows': quarantined,
             'editorial_plan_links': plans}
    pool = {'schema_version': SCHEMA_VERSION, 'as_of': as_of.isoformat(),
            'planning_week': iso_week(as_of), 'window_weeks': weeks,
            'meaning': 'Priority editorial review window, not trend validity or production approval.',
            'coverage': coverage,
            'saved_source_candidates_for_review': [entry['material_id'] for entry in raw],
            'legacy_candidates_needing_source_check': [entry['material_id'] for entry in legacy],
            'editorial_expansions_for_review': [entry['material_id'] for entry in edits],
            'excluded_current_material_ids': [entry['material_id'] for entry in current if entry['issues']],
            'older_materials_retained': sum(iso_monday(entry['source_week']) < iso_monday(weeks[0])
                                            for entry in entries),
            'future_materials_excluded': sum(iso_monday(entry['source_week']) > monday for entry in entries),
            'registry_path': relative(root, registry_path) if registry else None,
            'weather': {'status': 'not_checked_for_this_build', 'target_region': None,
                        'planned_publication_dates': [], 'source_url': None, 'checked_at': None},
            'media_authorization': 'Read current canonical workflow and editorial handoff; index grants none.',
            'production_quota': 'Not assigned by material index.'}
    valid_ids = {entry['material_id'] for entry in entries}
    for series in registry.get('series', []):
        if not set(series.get('source_material_ids', [])) <= valid_ids:
            raise ValueError(f"Unknown material reference in series {series.get('series_id')}")
    # Fail before derived writes if an input changed during this build.
    for path, expected in watched.items():
        if file_hash(root / path) != expected:
            raise ValueError(f'Input changed during build: {path}; retry from fresh inputs')
    rendered = render_summary(pool, index, registry)
    atomic_write(index_path, json.dumps(index, ensure_ascii=False, indent=2) + '\n')
    atomic_write(output / 'current_pool.json', json.dumps(pool, ensure_ascii=False, indent=2) + '\n')
    atomic_write(output / 'CURRENT_POOL.md', rendered)
    return pool, index


def render_summary(pool, index, registry):
    counts = Counter(entry['origin'] for entry in index['entries'] if entry['availability'] == 'present')
    lines = ['# Mira 跨週選材入口', '', f"更新基準：{pool['as_of']}；規劃週：{pool['planning_week']}。",
             '', '## 目前可用範圍', '',
             f"優先窗口：{'、'.join(pool['window_weeks'])}。這是選材優先順序，不是流行有效期限。", '',
             '| 來源週 | 原始單品列 | 狀態 |', '|---|---:|---|']
    for coverage in pool['coverage']:
        state = {'missing_original_csv': '缺原始 CSV',
                 'needs_receipt_reconciliation': '收據不符，暫不選用',
                 'saved_source_available_for_review': '可供編輯審閱'}[coverage['status']]
        lines.append(f"| {coverage['week']} | {coverage['saved_source_rows']} | {state} |")
    lines += ['', f"本窗口原始來源候選 {len(pool['saved_source_candidates_for_review'])} 筆；"
              f"需補來源的舊庫候選 {len(pool['legacy_candidates_needing_source_check'])} 筆；"
              f"編輯擴寫 {len(pool['editorial_expansions_for_review'])} 筆。單品列不等於完整穿搭。", '',
              f"全庫：有原始 CSV 對應 {counts['saved_weekly_source']} 筆，"
              f"舊庫來源待補 {counts['legacy_source_unverified']} 筆，"
              f"編輯擴寫 {counts['editorial_expansion']} 筆；"
              f"另隔離非正式週／測試 {len(index['quarantined_rows'])} 筆。", '',
              f"較早資料保留 {pool['older_materials_retained']} 筆，使用前重審季節與用途。"
              '相同服裝欄位只合併顯示，仍保留各週來源；近義名稱不自動當成同款。', '',
              '原始 CSV 可追溯不代表外部流行／商品主張已查證；原始列、編輯搭配與視覺核准分開。', '',
              '## 系列與使用紀錄', '',
              '以下全部是企劃候選；單支試片接受不等於整個系列採納或有效觸及。', '']
    for series in registry.get('series', []):
        lines.append(f"- {series['title']}：{series['audience_question']}")
    if not registry:
        lines.append('- 尚未建立獨立系列登錄檔。')
    lines += ['', '### 歷史研究回饋', '']
    for use in registry.get('uses', []):
        lines.append(f"- {use['usage_id']}：{use['feedback_summary']}")
    lines += ['', '## 下一次對話的執行入口', '',
              '1. 按 AGENTS 順序讀現行規則，再讀 `10_automation/MIRA_EDITORIAL_HANDOFF.md` 與本頁。',
              '2. 有新週 CSV 時先存入對應 run，重建索引；缺週明示，勿假裝完整三週資料。',
              '3. 選一個觀眾問題，從候選材料編完整搭配，將來源 material_id 寫入系列紀錄。',
              '4. 針對台灣實際地區、發布日期查天氣與場合條件，再決定系列、人物、套數與分鏡。',
              '5. 仍在內容企劃階段；新產量未定案，不由索引啟動影像生成。', '',
              '目前天氣：本次未查；發布日期、網址與成效未知者留空。', '',
              '詳列資料：`material_index.json`；當期選材：`current_pool.json`；'
              '人工維護系列／使用：`series_registry.json`。更新方法見同資料夾 `README.md`。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--as-of', default=date.today().isoformat(), help='Local planning date YYYY-MM-DD')
    parser.add_argument('--window-weeks', type=int, default=3)
    args = parser.parse_args()
    pool, index = build(args.root, args.as_of, args.window_weeks)
    print(json.dumps({'as_of': pool['as_of'], 'weeks': pool['window_weeks'],
                      'indexed_rows': len(index['entries']),
                      'quarantined_rows': len(index['quarantined_rows']),
                      'current_source_candidates': len(pool['saved_source_candidates_for_review']),
                      'missing_weeks': [item['week'] for item in pool['coverage']
                                        if item['status'] == 'missing_original_csv']}, ensure_ascii=True))


if __name__ == '__main__':
    main()
