"""Deterministic, material-batched Blender craft library. Game coordinates are Y-up."""
import bpy, bmesh, math, random, os, json
from mathutils import Vector, Matrix
from collections import defaultdict
from pathlib import Path

ROOT = Path('C:/Users/Fabio/projects/zepplin_journey')
OUT = ROOT / 'public/models/world-v2'
OUT.mkdir(parents=True, exist_ok=True)
MATS = {}
CACHE = {}

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
        import numpy as np
        n=256; yy,xx=np.mgrid[0:n,0:n]; rng=np.random.default_rng(42)
        if texture=='wood':
            noise=.95+.025*np.sin(xx*.5+np.sin(yy*.018)*3)+.012*np.sin(xx*1.9+np.sin(yy*.04)*5)+rng.random((n,n))*.015
        elif texture=='cloth': noise=.91+.045*np.sin(xx*2.7)+.045*np.sin(yy*2.7)
        else:
            coarse=np.repeat(np.repeat(rng.random((16,16)),16,axis=0),16,axis=1)
            for _ in range(16):coarse=(coarse+np.roll(coarse,1,0)+np.roll(coarse,-1,0)+np.roll(coarse,1,1)+np.roll(coarse,-1,1))/5
            noise=.88+coarse*.12+rng.random((n,n))*.035
        pixels=np.ones((n,n,4),dtype=np.float32)
        for k in range(3):
            value=np.clip(rgb[k]*noise,0,1)
            pixels[:,:,k]=np.where(value<=.04045,value/12.92,((value+.055)/1.055)**2.4)
        img=bpy.data.images.new('TEX-Journey-'+name,width=n,height=n,alpha=False)
        img.pixels.foreach_set(pixels.ravel()); img.pack()
        t=m.node_tree.nodes.new('ShaderNodeTexImage'); t.image=img
        m.node_tree.links.new(t.outputs['Color'],b.inputs['Base Color'])
    MATS[name]=m; return m

def palette():
    specs={
      'wood':('#98613b',0,.66,'wood'),'oak':('#c3955b',0,.68,'wood'),'darkwood':('#573d2e',0,.75,'wood'),
      'stone':('#cbb9a0',0,.9,'stone'),'stoneLight':('#ddccb0',0,.9,'stone'),'rock':('#897b70',0,.95,'stone'),
      'rockLight':('#ae9e88',0,.9,'stone'),'grass':('#71874b',0,.95,'grass'),'soil':('#634d32',0,1,'stone'),
      'brick':('#be6c49',0,.8,'stone'),'tile':('#b8623d',0,.78,'stone'),'tileLight':('#d08152',0,.78,'stone'),
      'cream':('#f2dfb4',0,.88,'cloth'),'teal':('#367c7b',0,.65,'cloth'),'red':('#b7473e',0,.8,'cloth'),
      'leaf':('#56732f',0,.83,None),'leafLight':('#829744',0,.85,None),'leafDark':('#334f29',0,.9,None),
      'purple':('#9b73ac',0,.8,None),'flower':('#ebbe57',0,.7,None),'white':('#efdfb9',0,.7,None),
      'iron':('#2f3939',1,.45,None),'brass':('#cf9a43',1,.32,None),'glass':('#93c5bc',0,.18,None),
      'skin':('#d09a70',0,.7,None),'hair':('#34261f',0,.75,None),'trousers':('#697351',0,.85,'cloth'),
      'scarf':('#b25437',0,.83,'cloth'),'leather':('#835432',0,.65,None),'screen':('#426f83',0,.25,None)}
    specs.update({'sand':('#e9d4a7',0,.98,'stone'),'meadow':('#86956a',0,.97,'grass'),'yard':('#8a8e86',0,.98,'stone'),
      'oliveLeaf':('#8c9b76',0,.92,None),'oliveDark':('#526348',0,.94,None),'cherry':('#a52f3c',0,.4,None),
      'grape':('#695477',0,.5,None),'waterDeep':('#277e96',.08,.28,None),'waterShallow':('#69c7bd',.05,.24,None),'foam':('#e7f3dc',0,.6,None)})
    for n,(c,me,r,t) in specs.items(): material(n,c,me,r,texture=t)
    material('lamp','#ffd383',rough=.35,emission=4)
    material('display','#89d6df',rough=.3,emission=.7)
    material('eye','#211e1a',rough=.3)

def template(kind):
    if kind in CACHE: return CACHE[kind]
    bm=bmesh.new()
    if kind=='box':
        bmesh.ops.create_cube(bm,size=1)
        bmesh.ops.bevel(bm,geom=list(bm.edges),offset=.055,segments=2,affect='EDGES')
    elif kind=='sphere': bmesh.ops.create_uvsphere(bm,u_segments=12,v_segments=8,radius=1)
    elif kind=='leaf': bmesh.ops.create_icosphere(bm,subdivisions=1,radius=1)
    elif kind=='rock': bmesh.ops.create_icosphere(bm,subdivisions=2,radius=1)
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
        self.mesh([rotation@Vector((x*size[0],y*size[1],z*size[2]))+p for x,y,z in v],f,mat,kind not in ('box','rock'))
    def box(self,p,s,mat='wood',rot=None): self.shape('box',p,s,mat,rot)
    def ball(self,p,s,mat='leaf',rot=None): self.shape('sphere',p,s,mat,rot)
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
    bpy.ops.export_scene.gltf(filepath=str(pending),export_format='GLB',use_selection=True,use_active_scene=True,export_apply=True,export_yup=True,export_animations=False,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6)
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
    b.collider('tree',(x,1.8*scale,z),(.55*scale,3.6*scale,.55*scale),'cylinder')
    rng=random.Random(seed); h=3.7*scale
    b.beam((x,0,z),(x+.15*scale,h*.8,z),.18*scale,'darkwood')
    for i in range(8):
        a=i*2.4; end=(x+math.cos(a)*1.15*scale,h*(.65+(i%3)*.12),z+math.sin(a)*1.15*scale)
        b.beam((x,h*.42,z),end,.07*scale,'wood')
    for i in range(95):
        a=rng.random()*math.tau; r=rng.random()**.5*1.55*scale; y=h+rng.uniform(-.6,.7)*scale
        p=(x+math.cos(a)*r,y,z+math.sin(a)*r)
        b.ball(p,(rng.uniform(.23,.43)*scale,.28*scale,.35*scale),['leaf','leafLight','leafDark'][i%3])
    for i in range(6):
        a=i*math.tau/6; b.beam((x, .5,z),(x+math.cos(a)*.55*scale,.04,z+math.sin(a)*.55*scale),.09*scale,'darkwood')

def flowerbed(b,x,z,radius=1,seed=1):
    rng=random.Random(seed)
    for i in range(24):
        a=rng.random()*math.tau; r=rng.random()**.5*radius; px=x+math.cos(a)*r; pz=z+math.sin(a)*r; h=rng.uniform(.2,.58)
        b.beam((px,0,pz),(px,h,pz),.014,'leafDark',4)
        b.shape('leaf',(px+.08,h*.55,pz),(.17,.025,.065),'leaf',rot=(0,a,.5))
        for j in range(5):
            a2=j*math.tau/5; b.shape('leaf',(px+math.cos(a2)*.07,h,pz+math.sin(a2)*.07),(.075,.035,.055),'purple' if i%3 else 'flower')
        b.ball((px,h+.02,pz),(.035,.03,.035),'flower')

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
    for i in range(20): b.box((7,.08,2.5+i*.37),(4.2,.2,.34),'oak' if i%3 else 'wood')
    for side in [-1,1]:
        for z in [2.5,5,7.5,9.5]:
            x=7+side*2.2; b.beam((x,-2,z),(x,1.05,z),.12,'darkwood'); b.ball((x,1.09,z),(.16,.12,.16),'brass')
            b.collider('pier-post',(x,.6,z),(.3,1.3,.3),'cylinder')
        for k in range(14):
            z=2.5+k*.5; y=.9-.15*math.sin(k/14*math.pi)
            b.beam((7+side*2.2,y,z),(7+side*2.2,.9-.15*math.sin((k+1)/14*math.pi),z+.5),.025,'oak')
    lantern(b,4.8,9.3); lantern(b,9.2,9.3); crate(b,8.5,.2,3.3); barrel(b,5.5,3.2,.8)

def base(b,r=13,seed=1,landscape=None):
    shape=landscape or {'rx':r,'rz':r,'power':2,'scallop':.03,'phase':0,'depth':9,'style':'garden','path':'stone','ground':'grass'}
    def boundary(a):return ((abs(math.cos(a)/shape['rx'])**shape['power']+abs(math.sin(a)/shape['rz'])**shape['power'])**(-1/shape['power']))*(1+shape['scallop']*math.cos(3*a+shape['phase']))
    rng=random.Random(seed); n=64; verts=[]
    radii=[boundary(i*math.tau/n) for i in range(n)]
    depth=shape['depth']
    for height,factor in [(0,1),(-.55,.99),(-depth*.25,.91),(-depth*.58,.62),(-depth,.18)]:
        for i in range(n):
            a=i*math.tau/n; rr=radii[i]*factor*(1 if height==0 else rng.uniform(.92,1.08)); verts.append((math.cos(a)*rr,height,math.sin(a)*rr))
    b.mesh(verts,[tuple(range(n-1,-1,-1))],shape['ground'])
    for j in range(4): b.mesh(verts,[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for i in range(n)],'stone' if j==0 else 'rockLight' if j==1 else 'rock')
    for i in range(38):
        a=i*2.4; rr=boundary(a)*rng.uniform(.56,.8); b.shape('rock',(math.cos(a)*rr,-depth*.34-rng.random()*depth*.22,math.sin(a)*rr),(rng.uniform(1.6,3),rng.uniform(1.5,2.9),rng.uniform(1.6,3)),'rockLight' if i%3==0 else 'rock')
    # Broken grassy shelves, mossy cliff pockets and low planting soften the rim.
    for i in range(90):
        a=rng.random()*math.tau; rr=boundary(a)-rng.uniform(.4,2.6); x=math.cos(a)*rr;z=math.sin(a)*rr
        if shape['style']=='coast' and x< -5:continue
        if shape['style']=='industrial' and i%3:continue
        if x>4 and z>2: continue
        b.ball((x,.14,z),(rng.uniform(.35,.8),.28,rng.uniform(.3,.65)),'leaf' if i%3 else 'leafDark')
        for k in range(4):
            b.shape('leaf',(x+rng.uniform(-.4,.4),.35,z+rng.uniform(-.4,.4)),(.07,rng.uniform(.2,.55),.06),'leafLight',rot=(0,a,rng.uniform(-.5,.5)))
        if i%4==0:
            b.shape('rock',(x,.08,z),(.6,.26,.45),'stone')
            b.ball((x,-1.1,z),(.7,.3,.6),'leafDark')
    # Irregular limestone paving and the path to the timber pier.
    for j in range(7 if shape['path']=='stone' else 0):
        for i in range(7):
            x=(i-3)*.8+math.sin(j)*.15; z=(j-1)*.8
            b.box((x,.035,z),(.74,.09,.7),'stoneLight' if (i+j)%3 else 'stone',rot=(0,rng.uniform(-.08,.08),0))
    if shape['path']=='carpet':b.box((1,.025,3),(2,.06,6),'red')
    elif shape['path']=='yard':
        for i in range(6):b.box((i-3,.025,4),(.85,.06,3.8),'yard')
    elif shape['path']=='earth':
        for i in range(9):b.ball((4-i*.65,.015,5-i*.45),(1,.025,.6),'soil')
    for i in range(7): b.box((2.8+i*.6,.04,4.6),(.58,.09,1.1),'oak' if shape['path']=='sand' else 'stone')
    dock(b)
    for i in range(12):
        a=i*math.tau/12; x=math.cos(a)*(boundary(a)-1.1);z=math.sin(a)*(boundary(a)-1.1)
        if shape['style']=='coast' and x< -5:continue
        if shape['style']=='industrial':continue
        if x>4 and z>2: continue
        flowerbed(b,x,z,1.2,seed*100+i)
        for k in range(9):
            yy=-k*.3; px=x+math.sin(k)*.15;pz=z+math.cos(k)*.15
            b.shape('leaf',(px,yy,pz),(.3,.16,.23),'leaf' if k%2 else 'leafDark')
    if shape['style'] not in ['orchard','coast','circus','industrial']:
        for i,(x,z,s) in enumerate([(-8,-4,1.2),(6,-7,1.3),(-9,4,.8),(8,0,.9)]): tree(b,x,z,s,seed*10+i)
    for x,z in [(-10,7),(10,1),(-7,-1),(9,-5.5)]:
        if shape['style'] in ['coast','circus']:continue
        if shape['style']=='coast' and x<-5:continue
        if shape['style']=='orchard' and x<0:continue
        lantern(b,x,z)
    # Wild lower gardens fill the sides without obstructing the central walk.
    for side in ([-1,1] if shape['style'] in ['garden','trail','campus'] else []):
        for j in range(5):
            x=side*(7+j%2*1.5);z=-8+j*2.4
            flowerbed(b,x,z,.9,seed*500+j)
            for k in range(6):
                b.ball((x+rng.uniform(-.9,.9),.3,z+rng.uniform(-.6,.6)),(.3,.4,.35),'leafDark' if k%2 else 'leaf')

def building(b,x,z,w=5,d=4,h=3,wall='stone',roof='tile'):
    b.collider('building',(x,h/2,z),(w,h,d))
    b.box((x,h/2,z),(w,h,d),wall)
    # Individual front masonry blocks and corner quoins.
    for row in range(int(h/.4)):
        for col in range(int(w/.65)):
            px=x-w/2+.33+col*.65+(row%2)*.15
            if abs(px-x)<.6 and row<5: continue
            b.box((px,.22+row*.4,z+d/2+.04),(.62,.37,.18),'stoneLight' if (row+col)%4 else 'stone')
    for side in [-1,1]:
        b.box((x+side*w/2,h*.5,z+d/2),(.17,h+.2,.2),'darkwood')
        wx=x+side*w*.29
        b.box((wx,1.8,z+d/2+.16),(1,1.2,.1),'darkwood'); b.box((wx,1.8,z+d/2+.22),(.78,.99,.04),'lamp')
        b.box((wx,1.8,z+d/2+.26),(.06,1.02,.05),'wood'); b.box((wx,1.8,z+d/2+.26),(.84,.06,.05),'wood')
        b.box((wx,1.12,z+d/2+.3),(1.2,.12,.4),'wood')
    b.box((x,1.05,z+d/2+.14),(1.1,2.1,.16),'teal')
    b.ball((x+.35,1,z+d/2+.26),(.045,.045,.045),'brass')
    for side in [-1,1]:
        for row in range(7):
            xx=side*(row+.5)*(w/2+.4)/7; yy=h+1.65-abs(xx)*.58
            for col in range(10):
                zz=z-d/2-.3+col*(d+.6)/10
                b.box((x+xx,yy,zz),((w/2+.4)/7+.07,.14,(d+.6)/10+.08),roof if (row+col)%3 else 'tileLight',rot=(0,0,-side*.52))
    b.beam((x,h+1.7,z-d/2-.45),(x,h+1.7,z+d/2+.45),.12,'tileLight',10)
    b.box((x+1.5,h+1.3,z-.7),(.65,1.8,.65),'brick'); b.box((x+1.5,h+2.25,z-.7),(.85,.16,.85),'stone')

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
