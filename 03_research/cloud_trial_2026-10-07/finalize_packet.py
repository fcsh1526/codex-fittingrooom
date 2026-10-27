"""Archive only approved trial inputs/tools; exclude local outputs and credentials."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    target = HERE / 'M02_cloud_trial_packet_v1.zip'
    if target.exists():
        raise FileExistsError(target)
    selected = [HERE / name for name in ('AGENTS.md', 'README.md', 'inputs_manifest.json', 'cloud_launch_prompt.txt')]
    for folder in ('inputs', 'evidence', 'workflow', 'prompts', 'tools'):
        selected.extend(path for path in (HERE / folder).rglob('*') if path.is_file() and '__pycache__' not in path.parts)
    inventory = [{'path': p.relative_to(HERE).as_posix(), 'sha256': sha(p), 'size_bytes': p.stat().st_size}
                 for p in sorted(selected)]
    manifest = json.loads((HERE / 'inputs_manifest.json').read_text(encoding='utf-8'))
    included = {item['path']: item for item in inventory}
    for item in manifest['files']:
        actual = included[item['path']]
        if actual['sha256'] != item['sha256'] or actual['size_bytes'] != item['size_bytes']:
            raise ValueError('Input changed before packaging')
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(selected):
            archive.write(path, path.relative_to(HERE).as_posix())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP CRC failure')
        for item in inventory:
            data = archive.read(item['path'])
            if len(data) != item['size_bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError('Archived bytes differ')
        if any(n.startswith('outputs/') or n.endswith(('.pyc', '.lock')) for n in archive.namelist()):
            raise ValueError('Unexpected local outputs in transfer packet')
    preflight = json.loads((HERE / 'outputs/preflight_A_1s_receipt.json').read_text(encoding='utf-8'))
    report = {'status': 'packet_prepared_locally_cloud_execution_not_started', 'archive': target.name,
              'archive_sha256': sha(target), 'archive_size_bytes': target.stat().st_size,
              'archived_files': inventory, 'verified_input_files': len(manifest['files']),
              'local_preflight': {'full_A_decoded_frames': preflight['source_A_full_decode']['decoded_frames'],
              'roundtrip_decoded_frames': preflight['round_trip_full_decode']['decoded_frames'],
              'source_size': preflight['source_A_full_decode']['metadata']['size'],
              'fps': preflight['source_A_full_decode']['metadata']['fps'], 'cloud_execution_verified': False},
              'cloud_task': None, 'new_B_submitted': False, 'new_B_retrieved': False,
              'combined_candidate_rendered': False, 'first_wave_modified': False}
    with (HERE / 'packet_verification.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({key: report[key] for key in ('status', 'archive_sha256', 'archive_size_bytes', 'verified_input_files', 'local_preflight')}))


if __name__ == '__main__':
    main()
