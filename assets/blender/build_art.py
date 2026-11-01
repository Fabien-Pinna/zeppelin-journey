"""Build raw candidates. Compress with prepare-art-assets.py before copying validated GLBs to public."""
import argparse
import json
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'assets/blender'))
parser=argparse.ArgumentParser()
parser.add_argument('--only',nargs='*')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
for obj in list(bpy.data.objects):
    if not obj.name.startswith('ZEP_'):bpy.data.objects.remove(obj,do_unlink=True)
for mat in list(bpy.data.materials):
    if mat.name.startswith('MAT-Journey-'):bpy.data.materials.remove(mat,do_unlink=True)
import craft
craft.COMPRESS=False
craft.OUT=ROOT/'artifacts/art-rebuild/candidates'
craft.OUT.mkdir(parents=True,exist_ok=True)
from islands import build_chapter,CHAPTERS
from characters import character
from travellers import airship

selected=args.only or [*CHAPTERS,'traveller','acrobat','zeppelin']
report=[]
for asset in selected:
    if asset in CHAPTERS:report.append(build_chapter(asset))
    elif asset=='zeppelin':airship()
    else:character(asset,backpack=asset!='acrobat')
    print('ART_BUILT',asset,flush=True)
output=ROOT/'artifacts/art-rebuild'
(output/'build-report.json').write_text(json.dumps(report,indent=2))
if not args.only:
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'artifacts/blender/zeppelin-art-library.blend'))
print('ART_BUILD_COMPLETE',flush=True)
