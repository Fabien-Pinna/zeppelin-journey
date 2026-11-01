"""Render exported candidates with consistent cameras; see browser captures for final runtime truth."""
import sys,math
from pathlib import Path
import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['atelier']
asset=args[0]
out=ROOT/'artifacts/art-rebuild'
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.render.resolution_x=1280;scene.render.resolution_y=900;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.world.use_nodes=True
bg=next(n for n in scene.world.node_tree.nodes if n.type=='BACKGROUND')
bg.inputs['Color'].default_value=(.36,.48,.65,1);bg.inputs['Strength'].default_value=.35
def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
for name,typ,position,power,color,size in [
    ('Sun','SUN',(-20,-25,35),3.0,(1,.83,.64),.12),
    ('Sky','AREA',(10,5,22),1800,(.64,.79,1),18),
    ('Bounce','AREA',(-10,-7,4),450,(1,.86,.69),16)]:
    data=bpy.data.lights.new(name,typ);data.energy=power;data.color=color
    if typ=='SUN':data.angle=size
    else:data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=position;aim(obj,(0,0,0))
path=out/'candidates'/f'{asset}.glb'
if not path.exists():path=ROOT/'public/models/world-v2'/f'{asset}.glb'
bpy.ops.import_scene.gltf(filepath=str(path))
for obj in list(scene.objects):
    if obj.type=='MESH':obj.hide_render=False
data=bpy.data.cameras.new('Review');camera=bpy.data.objects.new('Review',data);scene.collection.objects.link(camera);scene.camera=camera
if asset in ['traveller','acrobat']:
    camera.location=(2.5,-6,2.8);aim(camera,(0,0,1.2));data.lens=70
elif asset=='zeppelin':
    camera.location=(19,-25,13);aim(camera,(0,0,4));data.lens=45
else:
    camera.location=(27,-36,21);aim(camera,(0,0,-1.5));data.lens=48
    if asset=='clubmed':
        camera.location*=1.3;aim(camera,(0,0,-1.5))
scene.render.filepath=str(out/(asset+'-overview.png'));bpy.ops.render.render(write_still=True)
if asset=='atelier':
    camera.location=(9,-13,5.3);aim(camera,(-1,1.5,1.8));data.lens=34
    scene.render.filepath=str(out/'atelier-walking.png');bpy.ops.render.render(write_still=True)
print('ART_REVIEW_COMPLETE',asset,flush=True)
