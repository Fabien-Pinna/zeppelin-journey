"""Original travelling character and an adapted, passenger-oriented library zeppelin."""
import bpy, math, random
from mathutils import Vector
from craft import Batch, MATS, OUT, export, crate

def airship():
    b=Batch('airship'); objects=[]
    omit=['Cannon','Gunport','Bowsprit','Figurehead','BraidProfile']
    for o in list(bpy.context.scene.objects):
        if not o.name.startswith('ZEP_') or o.type!='MESH' or any(s in o.name for s in omit):continue
        mat=o.data.materials[0].name if o.data.materials else ''
        key=('cream' if 'Canvas' in mat else 'darkwood' if 'WoodDark' in mat else 'oak' if 'WoodLight' in mat else 'brass' if any(x in mat for x in ['Brass','Gold','Copper']) else 'glass' if 'Glass' in mat else 'iron' if any(x in mat for x in ['Iron','Steel','Metal']) else 'wood')
        if 'TailFin' in o.name: key='teal'
        if 'LanternGlass' in o.name:key='lamp'
        vertices=[]
        for v in o.data.vertices:
            p=o.matrix_world@v.co;vertices.append((p.x*.55,(p.z+9)*.55,-p.y*.55))
        faces=[tuple(p.vertices) for p in o.data.polygons]
        if 'Envelope_Hull' in o.name:
            groups={'cream':[],'teal':[]}
            for p in o.data.polygons:
                center=sum((Vector(vertices[i]) for i in p.vertices),Vector())/len(p.vertices)
                stripe=False
                groups['teal' if stripe else 'cream'].append(tuple(p.vertices))
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
    for z in [-.5,3.9]:
        b.beam((-.85,3.25,z),(.85,3.25,z),.055,'brass')
    for i in range(3):b.box((1.05+i*.23,1.92-i*.17,3.5),(.32,.12,1.1),'oak')
    crate(b,0,2.1,-1.1,.45)
    b.box((-.4,2.39,-1.1),(.42,.4,.3),'leather')
    # Cream ribs and a navigation pennant finish the passenger silhouette.
    objects=b.finish();export(objects,OUT/'zeppelin.glb')
    for o in objects:o.hide_set(True);o.hide_render=True
    return len(objects)

def character(asset="traveller", backpack=True):
    # A new adult storybook adventurer: tailored teal jacket, rust scarf,
    # sculpted facial features, wavy hair, leather satchel and hiking boots.
    all_objects=[]
    root=bpy.data.objects.new('Traveller',None);bpy.context.scene.collection.objects.link(root);all_objects.append(root)
    def part(name,pivot,build):
        joint=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(joint);joint.parent=root
        joint.location=(pivot[0],-pivot[2],pivot[1]);all_objects.append(joint)
        b=Batch(asset+'-'+name);build(b)
        objs=b.finish(parent=joint)
        for o in objs:
            for v in o.data.vertices:v.co-=Vector(joint.location)
        all_objects.extend(objs)
    def body(b):
        b.ball((0,1.22,0),(.32,.43,.22),'teal')
        b.box((0,.98,0),(.57,.17,.37),'leather')
        b.box((0,1.01,.205),(.13,.11,.04),'brass')
        for x in [-.2,.2]:
            b.box((x,1.22,.18),(.15,.17,.055),'teal')
            b.box((x,1.3,.216),(.16,.035,.03),'brass')
        for y in [1.12,1.3,1.45]:b.ball((0,y,.22),(.026,.026,.016),'brass')
        b.ball((0,1.62,0),(.12,.15,.12),'skin')
        b.ring((0,1.57,0),.145,.06,'scarf',segments=20)
        b.box((.12,1.37,.235),(.14,.4,.055),'scarf',rot=(0,0,.25))
        if backpack:
            b.box((0,1.3,-.28),(.49,.56,.24),'leather')
            b.box((0,1.56,-.29),(.51,.13,.26),'wood')
            b.box((0,1.28,-.422),(.17,.12,.025),'brass')
            for x in [-.22,.22]:b.beam((x,1.55,.1),(x,1.02,.19),.028,'leather')
            b.beam((-.22,1.59,-.27),(.22,1.59,-.27),.08,'cream')
    part('Body',(0,1.1,0),body)
    def head(b):
        b.ball((0,1.92,.015),(.265,.31,.235),'skin')
        b.ball((0,1.76,.07),(.19,.13,.16),'skin')
        for s in [-1,1]:
            b.ball((s*.257,1.89,0),(.055,.09,.05),'skin')
            b.ball((s*.094,1.96,.217),(.062,.042,.025),'white')
            b.ball((s*.094,1.96,.241),(.025,.03,.012),'eye')
            b.ball((s*.087,1.972,.252),(.007,.008,.004),'white')
            b.beam((s*.043,2.02,.225),(s*.143,2.035,.206),.016,'hair')
        b.ball((0,1.9,.245),(.052,.066,.055),'skin')
        # Small curved smile, lower-lip shadow and facial hair along the jaw.
        for i in range(8):
            x=-.07+i*.02;y=1.808- .014*math.sin(i/7*math.pi)
            b.ball((x,y,.23-abs(x)*.1),(.014,.006,.007),'hair')
        b.ball((0,2.117,-.02),(.27,.14,.235),'hair')
        rng=random.Random(71)
        for i in range(74):
            a=i*2.4;r=rng.uniform(.1,.25)
            b.ball((math.cos(a)*r,2.15+rng.uniform(-.04,.09),-.02+math.sin(a)*r),(.065,.06,.07),'hair')
        for s in [-1,1]: b.ball((s*.23,2.02,-.02),(.055,.13,.16),'hair')
    part('Head',(0,1.63,0),head)
    for side,label in [(-1,'Left'),(1,'Right')]:
        def arm(b,s=side):
            b.ball((s*.35,1.37,0),(.115,.25,.12),'teal',rot=(0,0,s*.14))
            b.ball((s*.4,1.07,.015),(.09,.19,.1),'teal')
            b.ring((s*.4,.93,.015),.078,.025,'cream',segments=16)
            b.ball((s*.4,.83,.02),(.075,.105,.075),'skin')
            b.ball((s*.34,.85,.06),(.036,.055,.035),'skin')
        part(label+'Arm',(side*.31,1.52,0),arm)
        def leg(b,s=side):
            b.ball((s*.155,.67,0),(.125,.34,.14),'trousers')
            b.ball((s*.155,.35,0),(.105,.22,.115),'trousers')
            b.ball((s*.155,.15,.045),(.13,.15,.21),'leather')
            b.box((s*.155,.055,.07),(.26,.09,.43),'darkwood')
            for y,z in [(.2,.17),(.23,.12),(.26,.06)]:b.beam((s*.155-.06,y,z),(s*.155+.06,y,z),.008,'cream',4)
        part(label+'Leg',(side*.155,.94,0),leg)
    export(all_objects,OUT/(asset+'.glb'))
    for o in all_objects:o.hide_set(True);o.hide_render=True
    return len(all_objects)
