"""Run headlessly against the preserved v2 scene; never reset the live scene."""
import sys
from pathlib import Path
import bpy

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'assets/blender'))
from craft import palette
from travellers import airship
from characters import character
from islands import build_chapter, CHAPTERS

# Keep only original zeppelin source objects in this isolated background process.
for obj in list(bpy.data.objects):
    if not obj.name.startswith('ZEP_'):bpy.data.objects.remove(obj,do_unlink=True)
palette()
airship()
character()
character('acrobat',backpack=False)
for chapter in CHAPTERS:print(build_chapter(chapter),flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'artifacts/blender/zeppelin-detail-library.blend'))
print('DETAIL_BUILD_COMPLETE',flush=True)
