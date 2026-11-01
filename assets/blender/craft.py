"""Deterministic, material-batched Blender craft library. Game coordinates are Y-up."""
import bpy, bmesh, math, random, os, json
from mathutils import Vector, Matrix
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/models/world-v2'
OUT.mkdir(parents=True, exist_ok=True)
MATS = {}
CACHE = {}
COMPRESS = True

def linear(c):
    return c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4

def material(name, color, metal=0, rough=.75, emission=0, texture=None):
    existing=bpy.data.materials.get('MAT-Journey-'+name)
    if existing: MATS[name]=existing; return existing
    m=bpy.data.materials.new('MAT-Journey-'+name); m.use_nodes=True
    b=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    b.inputs['Base Color'].default_value=(*[linear(c) for c in rgb],1)
    m.diffuse_color=(*rgb,1); b.inputs['Metallic'].default_value=metal; b.inputs['Roughness'].default_value=rough
    if emission:
        b.inputs['Emission Color'].default_value=(*[linear(c) for c in rgb],1)
        b.inputs['Emission Strength'].default_value=emission
    if texture:
        from surfaces import apply_surface
        apply_surface(m,b,rgb,texture)
    if name=='glass':
        b.inputs['Alpha'].default_value=.24
        b.inputs['Roughness'].default_value=.18
        m.use_backface_culling=False
    if texture=='cloth':b.inputs['Sheen Weight'].default_value=.22
    MATS[name]=m; return m

def palette():
    specs={
      'wood':('#967049',0,.66,'wood'),'oak':('#b48d60',0,.68,'wood'),'darkwood':('#594936',0,.75,'wood'),
      'stone':('#cbb9a0',0,.9,'stone'),'stoneLight':('#ddccb0',0,.9,'stone'),'rock':('#897b70',0,.95,'stone'),
      'rockLight':('#c4b79e',0,.9,'stone'),'grass':('#77815a',0,.95,'grass'),'soil':('#7b6650',0,1,'soil'),
      'brick':('#be6c49',0,.8,'stone'),'tile':('#b8623d',0,.78,'stone'),'tileLight':('#d08152',0,.78,'stone'),
      'cream':('#f0e2c7',0,.88,'cloth'),'teal':('#366e71',0,.65,'cloth'),'red':('#a84a40',0,.8,'cloth'),
      'leaf':('#577047',0,.83,None),'leafLight':('#8d9b60',0,.85,None),'leafDark':('#354c35',0,.9,None),
      'purple':('#9b73ac',0,.8,None),'flower':('#ebbe57',0,.7,None),'white':('#efdfb9',0,.7,None),
      'iron':('#434b4b',1,.45,'metal'),'brass':('#c5a268',1,.38,'metal'),'glass':('#c3ddd8',0,.18,None),
      'skin':('#d09a70',0,.7,None),'hair':('#34261f',0,.75,None),'trousers':('#697351',0,.85,'cloth'),
      'scarf':('#b25437',0,.83,'cloth'),'leather':('#835432',0,.65,None),'screen':('#426f83',0,.25,None)}
    specs.update({'sand':('#e9d4a7',0,.98,'stone'),'meadow':('#86956a',0,.97,'grass'),'yard':('#8a8e86',0,.98,'stone'),
      'oliveLeaf':('#8c9b76',0,.92,None),'oliveDark':('#526348',0,.94,None),'cherry':('#a52f3c',0,.4,None),
      'grape':('#695477',0,.5,None),'waterDeep':('#277e96',.08,.28,None),'waterShallow':('#69c7bd',.05,.24,None),'foam':('#e7f3dc',0,.6,None)})
    specs.update({'cliff':('#c9c2b1',0,.94,'cliff'),'cliffWarm':('#dfd2b6',0,.92,'cliff'),
      'cliffShade':('#aba997',0,.96,'cliff'),'rose':('#be7b89',0,.8,None),
      'plaster':('#ddd1b7',0,.92,'stone'),'copper':('#a58358',1,.4,'metal'),
      'canvas':('#f3e6ce',0,.87,'cloth')})
    for n,(c,me,r,t) in specs.items(): material(n,c,me,r,texture=t)
    material('lamp','#ffd383',rough=.35,emission=4)
    material('display','#25414a',rough=.3,emission=.3)
    material('pixelBlue','#9fc7ce',rough=.5,emission=.5)
    material('pixelGold','#ddbc7c',rough=.5,emission=.3)
    material('eye','#211e1a',rough=.3)

def template(kind):
    if kind in CACHE: return CACHE[kind]
    bm=bmesh.new()
    if kind=='box':
        bmesh.ops.create_cube(bm,size=1)
        bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.055,segments=2,affect='EDGES')
    elif kind=='sphere': bmesh.ops.create_uvsphere(bm,u_segments=20,v_segments=12,radius=1)
    elif kind=='bead': bmesh.ops.create_uvsphere(bm,u_segments=8,v_segments=6,radius=1)
    elif kind=='small-sphere': bmesh.ops.create_uvsphere(bm,u_segments=12,v_segments=8,radius=1)
    elif kind=='leaf': bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1)
    elif kind=='rock':
        bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1)
        for v in bm.verts:
            x,y,z=v.co
            v.co*=1+.065*math.sin(x*7+y*3)*math.cos(z*6)+.035*math.sin(y*11-z*4)
    bm.verts.ensure_lookup_table(); bm.verts.index_update()
    verts=[tuple(v.co) for v in bm.verts]; faces=[tuple(v.index for v in f.verts) for f in bm.faces]
    bm.free(); CACHE[kind]=(verts,faces); return verts,faces

class Batch:
    def __init__(self,name): self.name=name; self.data=defaultdict(lambda:[[],[],[]]); self.objects=[]; self.colliders=[]; self.parts=[]
    def collider(self,name,pos,size,kind='box'):
        self.colliders.append({'name':name,'type':kind,'position':list(pos),'size':list(size)})
    def mesh(self,verts,faces,mat,smooth=False):
        vs,fs,sm=self.data[mat]; offset=len(vs)
        unique={}
        for f in faces: unique.setdefault(tuple(sorted(f)),f)
        faces=list(unique.values())
        vs.extend((x,-z,y) for x,y,z in verts); fs.extend(tuple(i+offset for i in f) for f in faces); sm.extend([smooth]*len(faces))
    def shape(self,kind,pos,size,mat,rot=None):
        v,f=template(kind); p=Vector(pos)
        rotation=Matrix.Rotation(rot[1],3,'Y')@Matrix.Rotation(rot[0],3,'X')@Matrix.Rotation(rot[2],3,'Z') if rot else Matrix.Identity(3)
        self.mesh([rotation@Vector((x*size[0],y*size[1],z*size[2]))+p for x,y,z in v],f,mat,kind!='box')
    def box(self,p,s,mat='wood',rot=None): self.shape('box',p,s,mat,rot)
    def ball(self,p,s,mat='leaf',rot=None): self.shape('bead' if max(s)<.12 else 'small-sphere' if max(s)<.4 else 'sphere',p,s,mat,rot)
    def beam(self,a,b,r=.05,mat='wood',sides=8):
        a,b=Vector(a),Vector(b); axis=(b-a).normalized(); side=axis.cross(Vector((0,1,0)))
        if side.length<.01: side=axis.cross(Vector((1,0,0)))
        side.normalize(); up=axis.cross(side); verts=[]
        for p in (a,b):
            for i in range(sides): verts.append(p+(side*math.cos(i*math.tau/sides)+up*math.sin(i*math.tau/sides))*r)
        faces=[tuple(range(sides-1,-1,-1)),tuple(range(sides,sides*2))]
        faces += [(i,(i+1)%sides,(i+1)%sides+sides,i+sides) for i in range(sides)]
        self.mesh(verts,faces,mat,True)
    def ring(self,c,r,t,mat='brass',axis='y',segments=32):
        verts=[]
        for i in range(segments):
            a=i*math.tau/segments
            for j in range(6):
                b=j*math.tau/6; x=(r+t*math.cos(b))*math.cos(a); z=(r+t*math.cos(b))*math.sin(a); y=t*math.sin(b)
                v=(x,y,z) if axis=='y' else (x,z,y) if axis=='z' else (y,x,z)
                verts.append(tuple(c[k]+v[k] for k in range(3)))
        faces=[(i*6+j,((i+1)%segments)*6+j,((i+1)%segments)*6+(j+1)%6,i*6+(j+1)%6) for i in range(segments) for j in range(6)]
        self.mesh(verts,faces,mat,True)
    def finish(self,location=(0,0,0),parent=None):
        collection=bpy.data.collections.new('COL-'+self.name); bpy.context.scene.collection.children.link(collection)
        for mat,(verts,faces,smooth) in self.data.items():
            me=bpy.data.meshes.new('GEO-'+self.name+'-'+mat); me.from_pydata(verts,[],faces); me.materials.append(MATS[mat]); me.update()
            for p,sm in zip(me.polygons,smooth): p.use_smooth=sm
            uv=me.uv_layers.new(name='UVMap')
            for poly in me.polygons:
                normal=poly.normal; dominant=max(range(3),key=lambda i:abs(normal[i])); axes=[i for i in range(3) if i!=dominant]
                for li in poly.loop_indices:
                    v=me.vertices[me.loops[li].vertex_index].co; uv.data[li].uv=(v[axes[0]]*.7,v[axes[1]]*.7)
            obj=bpy.data.objects.new(me.name,me); collection.objects.link(obj); obj.location=(location[0],-location[2],location[1]); obj.parent=parent; self.objects.append(obj)
        return self.objects

def export(objects,path):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects: o.select_set(True)
    bpy.context.view_layer.objects.active=next((o for o in objects if o.type=='MESH'),objects[0])
    # Keep the last good asset intact while Blender encodes/writes the replacement.
    path=Path(path);pending=path.with_name(path.stem+'.pending.glb')
    bpy.ops.export_scene.gltf(filepath=str(pending),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=False,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=COMPRESS,export_draco_mesh_compression_level=6)
    pending.replace(path)
    print('EXPORTED',str(path),os.path.getsize(path))

def moving_part(batch, name, pivot, draw):
    """Keep a named pivot in glTF while batching the moving part by material."""
    part=Batch(batch.name+'-'+name); draw(part)
    root=bpy.data.objects.new('ANIM-'+name,None); bpy.context.scene.collection.objects.link(root)
    p=Vector((pivot[0],-pivot[2],pivot[1])); root.location=p
    objects=part.finish(parent=root)
    for obj in objects:
        for vertex in obj.data.vertices: vertex.co-=p
    # Nested articulated parts retain their own local pivots.
    for obj in part.parts:
        if obj.parent is None:
            obj.parent=root
            obj.location-=p
    batch.parts.extend([root,*objects,*part.parts])
    return root

def lantern(b,x,z,h=2.1):
    b.collider('lantern', (x,h/2,z),(.22,h,.22),'cylinder')
    b.beam((x,0,z),(x,h,z),.065,'iron')
    b.box((x,h+.06,z),(.5,.12,.5),'brass'); b.box((x,h-.48,z),(.38,.1,.38),'brass')
    b.ball((x,h-.23,z),(.12,.24,.12),'lamp')
    for dx in [-.16,.16]:
        for dz in [-.16,.16]: b.beam((x+dx,h-.46,z+dz),(x+dx,h,z+dz),.018,'iron',6)
    b.ball((x,h+.18,z),(.07,.08,.07),'brass')

def tree(b,x,z,scale=1,seed=1):
    from scenic_craft import tree as authored
    return authored(b, x, z, scale, seed)


def flowerbed(b,x,z,radius=1,seed=1):
    from scenic_craft import flowerbed as authored
    return authored(b, x, z, radius, seed)


def crate(b,x,y,z,s=.8):
    b.collider('crate',(x,y+s/2,z),(s,s,s))
    b.box((x,y+s/2,z),(s,s,s),'wood')
    for side in [-1,1]:
        for t in [-.36,.36]: b.box((x+t*s,y+s*.5,z+side*s*.51),(.09*s,s,.08),'oak')
        b.beam((x-s*.4,y+s*.1,z+side*s*.52),(x+s*.4,y+s*.9,z+side*s*.52),.045,'oak',4)

def barrel(b,x,z,s=1):
    b.collider('barrel',(x,.5*s,z),(.8*s,1.1*s,.8*s),'cylinder')
    b.ball((x,.5*s,z),(.38*s,.55*s,.38*s),'wood')
    for h in [.17,.8]: b.ring((x,h*s,z),.35*s,.025,'iron')
    b.box((x,1.02*s,z),(.58*s,.06,.58*s),'oak')

def dock(b):
    from scenic_craft import dock as authored
    return authored(b)


def base(b,r=13,seed=1,landscape=None):
    from scenic_craft import base as authored
    return authored(b, r, seed, landscape)


def building(b,x,z,w=5,d=4,h=3,wall='stone',roof='tile'):
    from scenic_craft import building as authored
    return authored(b, x, z, w, d, h, wall, roof)


def bunting(b,a,c):
    a,c=Vector(a),Vector(c)
    for i in range(24):
        t=i/24;p=a.lerp(c,t);p.y-=math.sin(t*math.pi)*.75
        q=a.lerp(c,(i+1)/24);q.y-=math.sin((i+1)/24*math.pi)*.75
        b.beam(p,q,.015,'darkwood',4)
        if i%2:
            b.mesh([p+Vector((-.14,0,0)),p+Vector((.14,0,0)),p+Vector((0,-.4,0))],[(0,1,2),(2,1,0)],['red','teal','cream'][i%3])
        else: b.ball(p+Vector((0,-.1,0)),(.06,.08,.06),'lamp')

def bicycle(b,x,z):
    b.collider('bicycle',(x,.8,z),(2,1.6,.5))
    for dx in [-.7,.7]:
        b.ring((x+dx,.55,z),.5,.045,'iron','z',24)
        for i in range(8):
            a=i*math.tau/8;b.beam((x+dx,.55,z),(x+dx+math.cos(a)*.48,.55+math.sin(a)*.48,z),.008,'brass',4)
    for a,c in [((-.7,.55),(-.2,1.2)),((-.2,1.2),(.15,.55)),((.15,.55),(-.7,.55)),((-.2,1.2),(.55,1.2)),((.55,1.2),(.15,.55)),((.55,1.2),(.7,.55))]: b.beam((x+a[0],a[1],z),(x+c[0],c[1],z),.035,'teal')
    b.box((x-.2,1.3,z),(.35,.08,.22),'leather');b.beam((x+.55,1.2,z),(x+.55,1.5,z),.035,'brass');b.beam((x+.55,1.5,z-.2),(x+.55,1.5,z+.2),.025,'iron')

palette()
