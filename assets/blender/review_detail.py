"""Render the shipped GLBs, not pre-export geometry, for silhouette/material QA."""
import bpy, math, sys, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'artifacts/detail-review';OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED';scene.render.threads=4
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.color=(.35,.35,.35)
scene.view_settings.view_transform='AgX'
def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size,color in [('Key',(3,-4,6),650,5,(1,.84,.66)),('Fill',(-4,-1,3),400,4,(.67,.80,1)),('Rim',(1,4,5),800,3,(1,.9,.72))]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=pos;aim(obj,(0,0,1))
data=bpy.data.cameras.new('CAM-detail');cam=bpy.data.objects.new('CAM-detail',data);scene.collection.objects.link(cam);scene.camera=cam
data.type='ORTHO'
bpy.ops.mesh.primitive_plane_add(size=200)
floor=bpy.context.object;floor.name='GEO-review-floor'
mat=bpy.data.materials.new('Review-floor');mat.diffuse_color=(.12,.15,.15,1);floor.data.materials.append(mat)
def load(asset):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'public/models/world-v2'/f'{asset}.glb'))
    objects=set(bpy.data.objects)-before
    for obj in objects:obj.rotation_mode='XYZ'
    return objects
def render(name,position,target,scale):
    cam.location=position;aim(cam,target);cam.data.ortho_scale=scale
    scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
def remove(objects):
    for obj in objects:bpy.data.objects.remove(obj,do_unlink=True)
objects=load('traveller')
render('traveller-front',(3,-7,3.1),(0,0,1.13),2.8)
render('traveller-back',(-3,7,3.0),(0,0,1.15),2.8)
render('traveller-face',(1.4,-6,2.6),(0,-.03,1.94),.85)
remove(objects)
objects=load('farm')
root=next(o for o in objects if o.name=='ANIM-sheep-a')
keep={root,*root.children_recursive}
remove(objects-keep);root.location=(0,0,0)
render('sheep',(3,-5,2.4),(.1,0,.63),2.0)
head=next(o for o in keep if o.name=='ANIM-sheep-a-head');head.rotation_euler.y=.65
render('sheep-grazing',(3,-5,2.4),(.1,0,.63),2.0)
remove(keep)
objects=load('acrobat')
for obj in objects:
    if obj.name.startswith(('LeftArm','RightArm')):
        obj.rotation_euler.x=math.pi;obj.location.z=1.64
bpy.context.view_layer.update()
grips={}
for side in ['Left','Right']:
    joint=next(o for o in objects if o.name.startswith(side+'Arm') and o.type=='EMPTY')
    points=[o.matrix_world@v.co for o in joint.children_recursive if o.type=='MESH' and 'skinDetail' in o.name for v in o.data.vertices]
    bounds=[[min(v[k] for v in points),max(v[k] for v in points)] for k in range(3)]
    grips[side]=bounds
    assert bounds[2][0] < 2.33 < bounds[2][1], (side,bounds)
(OUT/'grips.json').write_text(json.dumps(grips,indent=2))
render('acrobat-grip',(3,-6,3),(0,0,1.35),3.1)
remove(objects)
objects=load('zeppelin')
rotors=[o for o in objects if o.name.startswith('ANIM-propeller')]
assert len(rotors)==2
for i,angle in enumerate([0,.38,.76]):
    for j,rotor in enumerate(rotors):rotor.rotation_euler.y=-angle*(1 if j else -1)
    render('propellers-'+str(i),(9,22,12),(0,0,3.8),21)
remove(objects)
print('DETAIL_REVIEW_COMPLETE',flush=True)
