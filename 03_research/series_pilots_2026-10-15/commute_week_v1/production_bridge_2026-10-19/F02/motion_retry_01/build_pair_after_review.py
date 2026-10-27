"""Reuse the established native-frame pair builder for the new source only."""
from pathlib import Path
import importlib.util, argparse, json
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mira_gait_pair_builder',HERE.parent/'build_first_pair_review.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
h.HERE=HERE
h.F01=HERE.parent.parent/'F01/F01_source.mp4'
h.F02=HERE/'F02_source.mp4'
h.OUTPUT=HERE/'F01_F02_gait_fix_review_v1.mp4'
h.RECEIPT=HERE/'F01_F02_gait_fix_review_v1_receipt.json'
h.QA=HERE/'QA_pair'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--f02-sha',required=True)
args=parser.parse_args()
print(json.dumps(h.build(args.f02_sha),ensure_ascii=False))
