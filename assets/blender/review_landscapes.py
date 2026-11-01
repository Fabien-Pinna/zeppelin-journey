"""Inspect exported personal places, independent of the live Blender scene."""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/detail-review';OUT.mkdir(exist_ok=True,parents=True)
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=20;scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.resolution_x=1200;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.world.color=(.5,.5,.5);scene.view_settings.view_transform='AgX'
def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size in [('Key',(-20,-20,40),18000,25),('Fill',(25,0,30),15000,30)]:
    light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size
    obj=bpy.data.objects.new(name,light);scene.collection.objects.link(obj);obj.location=pos;aim(obj,(0,0,0))
data=bpy.data.cameras.new('CAM-landscape-review');cam=bpy.data.objects.new('CAM-landscape-review',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO'
animals_only='--animals' in sys.argv
for chapter in (['circus'] if animals_only else ['farm','circus','clubmed']):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'public/models/world-v2'/f'{chapter}.glb'))
    objects=set(bpy.data.objects)-before
    data.ortho_scale=48 if chapter=='clubmed' else 40;cam.location=(25,-40,32);aim(cam,(0,0,-1))
    if not animals_only:
        scene.render.filepath=str(OUT/f'{chapter}-export.png');bpy.ops.render.render(write_still=True)
    if chapter=='circus':
        data.ortho_scale=7;cam.location=(-3,-7,5);aim(cam,(-9,0,1.5));scene.render.filepath=str(OUT/'elephant-export.png');bpy.ops.render.render(write_still=True)
        data.ortho_scale=4.3;cam.location=(3,-14,3.8);aim(cam,(-1,-9,.9));scene.render.filepath=str(OUT/'lion-export.png');bpy.ops.render.render(write_still=True)
    for obj in objects:bpy.data.objects.remove(obj,do_unlink=True)
print('LANDSCAPE_REVIEW_COMPLETE',flush=True)
