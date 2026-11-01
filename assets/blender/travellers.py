"""Original travelling character and an adapted, passenger-oriented library zeppelin."""
import bpy, math, random
from mathutils import Vector, Matrix
from craft import Batch, MATS, OUT, export, crate, moving_part
from organic import Organic

def airship():
    b=Organic('airship'); objects=[]
    omit=['Cannon','Gunport','Bowsprit','Figurehead','BraidProfile','Props_']
    for o in list(bpy.context.scene.objects):
        if not o.name.startswith('ZEP_') or o.type!='MESH' or any(s in o.name for s in omit):continue
        mat=o.data.materials[0].name if o.data.materials else ''
        key=('cream' if 'Canvas' in mat else 'darkwood' if 'WoodDark' in mat else 'oak' if 'WoodLight' in mat else 'brass' if any(x in mat for x in ['Brass','Gold','Copper']) else 'glass' if 'Glass' in mat else 'iron' if any(x in mat for x in ['Iron','Steel','Metal']) else 'wood')
        if 'TailFin' in o.name: key='teal'
        if 'Envelope_Seam' in o.name: key='brass'
        if 'Rigging' in o.name and 'Rope' in mat: key='cream'
        if 'Copper' in mat: key='copper'
        if 'LanternGlass' in o.name:key='lamp'
        vertices=[]
        for v in o.data.vertices:
            p=o.matrix_world@v.co;vertices.append((p.x*.55,(p.z+9)*.55,-p.y*.55))
        faces=[tuple(p.vertices) for p in o.data.polygons]
        if 'Envelope_Hull' in o.name:
            groups={'canvas':[],'cream':[]}
            for p in o.data.polygons:
                center=sum((Vector(vertices[i]) for i in p.vertices),Vector())/len(p.vertices)
                stripe=int((center.z+12)*.7)%3==0
                groups['cream' if stripe else 'canvas'].append(tuple(p.vertices))
            for k,fs in groups.items():b.mesh(vertices,fs,k,True)
        else:b.mesh(vertices,faces,key,True)
    # Glazed observation cabin, handrails, boarding steps and travel luggage.
    b.box((0,2.16,1.7),(1.55,.18,4.5),'oak')
    b.box((0,2.65,1.7),(1.45,.95,4.1),'glass')
    for side in [-1,1]:
        for z in [-.3,.7,1.7,2.7,3.7]:
            b.beam((side*.76,2.18,z),(side*.76,3.17,z),.045,'brass')
        for y in [2.2,3.15]:b.beam((side*.76,y,-.35),(side*.76,y,3.75),.05,'darkwood')
        for z in [.2,1.2,2.2,3.2]:
            b.ball((side*.77,2.8,z),(.025,.17,.22),'lamp')
    b.box((0,3.23,1.7),(1.85,.2,4.5),'teal')
    for z in [.2,1.4,2.6]:
        for side in [-1,1]:
            b.box((side*.45,2.4,z),(.38,.12,.52),'leather')
            b.box((side*.6,2.68,z),(.07,.55,.52),'teal')
            b.beam((side*.45,2.22,z),(side*.45,2.4,z),.04,'brass',12)
        b.box((0,2.6,z),(.38,.06,.45),'oak')
    for z in [-.5,3.9]:
        b.beam((-.85,3.25,z),(.85,3.25,z),.055,'brass')
    for i in range(3):b.box((1.05+i*.23,1.92-i*.17,3.5),(.32,.12,1.1),'oak')
    crate(b,0,2.1,-1.1,.45)
    b.box((-.4,2.39,-1.1),(.42,.4,.3),'leather')
    # Longitudinal twin engines: visible from aft, clear of the envelope and fins.
    for side,label in [(-1,'L'),(1,'R')]:
        x=side*3.5;y=3.4;z=-3.5
        for offset in [-.45,.45]:
            b.beam((side*1.35,2.35,z+offset),(x,y,z+offset),.10,'iron',16)
            b.beam((side*1.7,3.4,z+offset),(x,y,z+offset),.065,'brass',12)
        b.ball((x,y,z),(.32,.32,.72),'teal')
        for zz in [-.5,0,.5]:b.ring((x,y,z+zz),.3,.045,'brass','z',32)
        b.beam((x,y,z-.65),(x,y,z-1),.10,'iron',20)
        pivot=(x,y,z-1)
        b.ring(pivot,1.14,.025,'brass','z',48)
        def rotor(part,pivot=pivot):
            hub=Organic('propeller-hub');hub.ball(pivot,(.17,.17,.20),'brass')
            for mat,(vertices,faces,_) in hub.data.items():part.mesh([(a,c,-bb) for a,bb,c in vertices],faces,mat,True)
            for i in range(3):
                blade=Organic('propeller-blade')
                blade.profile([(.08,0,0,.06,.045),(.32,.04,.015,.13,.04),(.68,.085,.025,.15,.028),(.96,.07,.04,.10,.02),(1.06,.03,.04,.01,.005)],'oak',20,3)
                rotation=Matrix.Rotation(i*math.tau/3,3,'Z')
                for mat,(vertices,faces,_) in blade.data.items():
                    part.mesh([Vector(pivot)+rotation@Vector((a,c,-bb)) for a,bb,c in vertices],faces,mat,True)
        moving_part(b,'propeller-'+label,pivot,rotor)
    objects=b.finish()+b.parts;export(objects,OUT/'zeppelin.glb')
    for o in objects:o.hide_set(True);o.hide_render=True
    return len(objects)


from characters import character
