"""Career dioramas. Import craft first; call build_chapter per bounded MCP task."""
import bpy, math, random, json
from mathutils import Vector
from craft import Batch, base, building, bunting, tree, flowerbed, lantern, crate, barrel, bicycle, export, OUT, ROOT, moving_part

CHAPTERS=['atelier','warehouse','masonry','farm','clubmed','circus','backroads','learning','oclock']

def desk(b,x,z):
    b.collider("desk",(x,.85,z),(2,1.7,.8))
    b.collider("chair",(x,.65,z+1),(.7,1.3,.75))
    b.box((x,.85,z),(2,.14,.8),'oak')
    for dx in [-.85,.85]:
        for dz in [-.28,.28]: b.beam((x+dx,0,z+dz),(x+dx,.83,z+dz),.045,'iron')
    b.box((x,1.35,z-.2),(1,.65,.07),'iron');b.box((x,1.35,z-.155),(.89,.53,.02),'display')
    b.box((x,.96,z+.15),(.75,.035,.25),'cream')
    b.beam((x,1,z-.2),(x,1.25,z-.2),.035,'iron')
    b.box((x,.5,z+1),(.65,.13,.65),'leather');b.box((x,.94,z+1.3),(.65,.8,.1),'teal')
    for dx in [-.22,.22]: b.beam((x+dx,0,z+.8),(x+dx,.5,z+1),.04,'iron')

def pavilion(b):
    # Open-front conservatory with visible studio interior and tiled canopy.
    b.box((-2,.08,-3),(8,.22,6),'wood')
    for row in range(12): b.box((-2,.21,-5.8+row*.47),(7.8,.08,.42),'oak' if row%3 else 'wood')
    for x in [-5.7,-2,1.7]:
        for z in [-5.7,-.3]:
            b.beam((x,.25,z),(x,4.1,z),.13,'darkwood');b.box((x,4,z),(.5,.23,.5),'brass')
    for x in [-5.7,1.7]:
        b.box((x,1,-3),(.2,1.8,5.5),'stone')
        for z in [-4.8,-3.2,-1.6]:
            b.box((x,2.7,z),(.06,1.5,1.4),'glass')
            b.beam((x,1.9,z+.75),(x,3.6,z+.75),.04,'brass')
    b.box((-2,2,-5.8),(7.6,3.8,.17),'teal')
    for x in [-4.4, -2, .4]: desk(b,x,-3.3)
    for side in [-1,1]:
        for row in range(8):
            x=-2+side*(row+.5)*.52;y=5.6-abs(x+2)*.35
            for col in range(12): b.box((x,y,-6.1+col*.55),(.59,.12,.63),'teal',rot=(0,0,-side*.34))
        for z in [-6.1,-4,-2,.1]: b.beam((-2,5.65,z),(-2+side*4.2,4.18,z),.045,'brass')
    for x in [-5.8,1.8]: lantern(b,x,-.1,3.1)
    for x in [-5.7,1.7]: b.collider("pavilion-wall",(x,2,-3),(.28,4,5.5))
    b.collider("pavilion-back",(-2,2,-5.8),(7.6,4,.25))
    for x in [-5.7,-2,1.7]: b.collider("pavilion-post",(x,2,-.3),(.3,4,.3),"cylinder")
    b.collider("display",(2.5,1.2,1),(1.3,2.4,.7))
    # Books, display plinth and a small animal-encyclopedia exhibit.
    b.box((2.5,.8,1),(1.3,1.6,.7),'wood');b.box((2.5,1.9,1),(1.1,.85,.09),'iron');b.box((2.5,1.9,1.06),(.94,.7,.02),'display')
    for i in range(7): b.box((-4.5+i*.17,.5,-.8),(.13,.5+((i%3)*.08),.28),['red','teal','cream'][i%3])

def warehouse(b):
    building(b,-2,-4,7,4,3.6,'brick')
    b.box((-2,1.65,-1.8),(2.7,3.2,.2),'darkwood')
    for row in range(8): b.box((-2,.25+row*.4,-1.66),(2.6,.34,.1),'teal')
    for i in range(8): crate(b,-5+(i%3)*1.1,0 if i<5 else 1.05,1+(i//3)*1.15,1)
    # Pallet stack and an electric warehouse truck with forks and mast.
    for y in [.08,.32,.56]:
        for j in range(5): b.box((2.5+j*.21,y,-1.5),( .17,.12,1.1),'oak')
    b.collider("forklift",(2.5,1.25,1.9),(1.8,2.5,3.5))
    b.collider("pallets",(2.9,.35,-1.5),(1.1,.7,1.1))
    b.box((2.5,.65,2.3),(1.5,.9,2),'flower');b.box((2.5,1.3,2.8),(1.3,.4,.7),'iron')
    for x in [1.85,3.15]:
        for z in [1.65,2.95]: b.ball((x,.35,z),(.22,.35,.35),'iron')
        b.beam((x,.2,1.3),(x,2.7,1.3),.08,'iron')
        b.box((x,.18,.55),(.15,.12,1.7),'iron')
        b.beam((x,1,3),(x,2.4,3),.05,'iron')
    b.box((2.5,2.45,2.3),(1.6,.13,1.9),'flower')

def masonry(b):
    building(b,-4,-4,4.7,4,3)
    for x in [-.4,2.4]: b.collider("arch-pier",(x,1.4,-2),(.7,2.8,.85))
    for x in [-1,4]: b.collider("crane-post",(x,3,-4),(.32,6,.32))
    b.collider("stone-stack",(.5,.6,1),(2.6,1.2,.6))
    b.collider("wheelbarrow",(3,.7,2),(1,1.4,2.2))
    # Individually laid stone arch, rather than a painted flat wall.
    for side in [-1,1]:
        for row in range(6): b.box((1+side*1.4,.22+row*.43,-2),(.62,.4,.8),'stoneLight' if row%2 else 'stone')
    for i in range(11):
        a=i*math.pi/10;b.box((1+math.cos(a)*1.4,2.55+math.sin(a)*1.4,-2),(.5,.58,.82),'stoneLight',rot=(0,0,a-math.pi/2))
    for x in [-1,4]:
        b.beam((x,0,-4),(x,6,-4),.14,'wood')
        b.beam((x,1,-4),(x,4.7,-.6),.09,'wood')
    b.beam((-1,5.9,-4),(5.5,5.9,-4),.2,'oak')
    b.beam((-1,6.5,-4),(5.5,6.5,-4),.065,"iron")
    for x in [-1,5.5]: b.beam((x,5.9,-4),(x,6.5,-4),.065,"iron")
    for i in range(4): b.beam((i*1.4-1,5.9,-4),(i*1.4+.4,6.5,-4),.065,'iron')
    b.beam((3.5,5.9,-4),(3.5,2.2,-4),.025,'iron')
    b.box((3.5,1.9,-4),(1.1,.65,.8),'stone')
    for i in range(12): b.box((-.5+i%4*.65,.2+(i//4)*.4,1),(.6,.36,.5),'stoneLight')
    for side in [-1,1]:
        b.beam((3+side*.38,.65,1.7),(3+side*.38,.8,3),.045,'wood')
    b.box((3,.7,1.7),(.9,.5,1),'teal');b.ring((3,.35,1),.3,.08,'iron','x',16)

def sheep(b,x,z,s=1):
    b.ball((x,.7*s,z),(.6*s,.45*s,.38*s),'cream')
    for i in range(16):
        a=i*2.4;b.ball((x+math.cos(a)*.42*s,.78*s+math.sin(i)*.22*s,z+math.sin(a)*.27*s),(.18*s,.18*s,.18*s),'white')
    b.ball((x+.52*s,.8*s,z),(.25*s,.3*s,.22*s),'darkwood')
    for dx in [-.32,.32]:
        for dz in [-.21,.21]: b.beam((x+dx*s,.1,z+dz*s),(x+dx*s,.65*s,z+dz*s),.06*s,'darkwood')

def farm(b):
    building(b,1,-4,5,4,3,'cream')
    b.box((1,1.2,-1.8),(2.1,2.3,.18),'leafDark')
    b.beam((.1,.2,-1.65),(1.9,2.3,-1.65),.06,'cream');b.beam((1.9,.2,-1.65),(.1,2.3,-1.65),.06,'cream')
    # Windmill with an open timber lattice.
    b.beam((-5,0,-5),(-5,6,-5),1,'stone',12)
    b.ball((-5,6.15,-5),(1.35,.6,1.35),'tile')
    def rotor(b):
        for i in range(4):
            a=i*math.pi/2+.5; dx,dz=math.cos(a),math.sin(a)
            b.beam((-5,5.1,-3.9),(-5+dx*3,5.1+dz*3,-3.9),.09,'darkwood')
            for k in range(4):
                r=1.2+k*.43
                b.beam((-5+dx*r-dz*.32,5.1+dz*r+dx*.32,-3.9),(-5+dx*r+dz*.32,5.1+dz*r-dx*.32,-3.9),.045,'oak')
            for s in [-1,1]:b.beam((-5+dx*1-dz*s*.32,5.1+dz*1+dx*s*.32,-3.9),(-5+dx*2.9-dz*s*.32,5.1+dz*2.9+dx*s*.32,-3.9),.04,'oak')
    moving_part(b,"windmill",(-5,5.1,-3.9),rotor)
    b.collider("windmill",(-5,3,-5),(2,6,2),"cylinder")
    for row in range(4):
        z=1+row*.85;b.box((-3,.06,z),(4,.17,.6),'soil')
        for col in range(8):
            x=-4.7+col*.5
            for k in range(3):b.shape('leaf',(x+math.sin(k*2)*.1,.3,z),(.22,.25,.1),'leafLight',rot=(0,k*2,.3))
    moving_part(b,"sheep-a",(2,0,2),lambda part:sheep(part,2,2))
    moving_part(b,"sheep-b",(3.8,0,3),lambda part:sheep(part,3.8,3,.8))
    b.collider("fence",(5.2,.55,2.2),(.16,1.1,6.6))
    for i in range(9):
        z=-1+i*.8;b.beam((5.2,0,z),(5.2,1.1,z),.065,'wood')
        if i<8:
            for y in [.45,.9]:b.beam((5.2,y,z),(5.2,y,z+.8),.04,'oak')

def circus(b):
    # Open front reveals a raised ring, curtains and illuminated proscenium.
    n=40; r=4.3; center=(0,0,-3)
    for i in range(n):
        a=i*math.tau/n; c=(i+1)*math.tau/n
        color='red' if (i//2)%2 else 'cream'
        b.mesh([(0,6,-3),(r*math.cos(a),3.1,-3+r*math.sin(a)),(r*math.cos(c),3.1,-3+r*math.sin(c))],[(0,1,2)],color)
        if math.sin(a)<.55:
            b.mesh([(r*math.cos(a),0,-3+r*math.sin(a)),(r*math.cos(c),0,-3+r*math.sin(c)),(r*math.cos(c),3.1,-3+r*math.sin(c)),(r*math.cos(a),3.1,-3+r*math.sin(a))],[(0,1,2,3)],color)
    b.collider("tent-pole",(0,3.4,-3),(.2,6.8,.2),"cylinder")
    for i in range(n):
        a=(i+.5)*math.tau/n
        if math.sin(i*math.tau/n)<.55: b.collider("tent-wall",(math.cos(a)*4.3,1.5,-3+math.sin(a)*4.3),(.72,3,.72),"cylinder")
    b.beam((0,0,-3),(0,6.8,-3),.07,'brass')
    b.mesh([(0,6.8,-3),(1.2,6.5,-3),(0,6.2,-3)],[(0,1,2),(2,1,0)],'red')
    b.ring((0,.2,-3),3.8,.14,'brass');b.ring((0,3.1,-3),4.3,.08,'brass')
    for i in range(24):
        a=i*math.tau/24;b.ball((math.cos(a)*4.3,3,-3+math.sin(a)*4.3),(.085,.085,.085),'lamp')
    for row in range(3):
        for col in range(8):
            x=-3+col*.85;z=3+row*.8;b.collider("seat",(x,.65,z),(.65,1.3,.65));b.box((x,.5,z),(.65,.12,.6),'wood');b.box((x,.9,z+.27),(.65,.7,.09),'red')
    for x in [-3.8,3.8]:lantern(b,x,1,2.8)

def clubmed(b):
    b.box((0,.01,-3),(9,.1,7),'cream')
    for x in [-3.7,3.7]:
        for z in [-5,0]: b.beam((x,0,z),(x,7,z),.08,'iron')
        b.beam((x,7,-5),(x,7,0),.07,'iron')
        b.beam((x,7,-5),(x*1.7,0,-7),.016,'iron')
    for z in [-5,-2.5,0]:b.beam((-3.7,7,z),(3.7,7,z),.08,'iron')
    for x in [-3.7,3.7]:
        for z in [-5.8,.8]:
            b.beam((x,0,z),(x,2.1,z),.055,"iron")
            b.beam((x,2.1,z),(x*.946,1.8,z+.2 if z<0 else z-.2),.035,"oak")
            b.collider("net-post",(x,1,z),(.15,2,.15),"cylinder")
    b.box((-4.1,4.7,-2.4),(1.2,.14,1.2),"wood")
    for i in range(23):
        x=-3.5+i*.32;b.beam((x,1.8,-5.6),(x,1.8,.6),.012,'cream',4)
    for i in range(22):
        z=-5.6+i*(6.2/21);b.beam((-3.5,1.8,z),(3.5,1.8,z),.012,'cream',4)
    # Ropes, bar and performer share one runtime pendulum pivot.
    for x in [-3.7,3.7]:
        for z in [-5,0]: b.collider("trapeze-post",(x,3.5,z),(.2,7,.2),"cylinder")
    b.collider("safety-net",(0,1.8,-2.5),(7,.12,6.2))
    for i in range(12): b.box((-4.3,.2+i*.4,-.5-i*.15),(.75,.1,.4),"oak")
    b.beam((-4.65,0,-.35),(-4.65,4.8,-2.2),.06,"iron")
    b.beam((-3.95,0,-.35),(-3.95,4.8,-2.2),.06,"iron")
    b.collider("ladder",(-4.3,2.4,-1.2),(.85,4.8,2.2))
    for x in [-6,6]:
        b.beam((x,0,-5),(x+.3,5,-5),.16,'wood')
        for k in range(9):
            a=k*math.tau/9
            for j in range(5):
                r=j*.4;b.shape('leaf',(x+math.cos(a)*r,5+.2*math.sin(r)-r*.2,-5+math.sin(a)*r),(.65,.05,.18),'leaf',rot=(0,-a,0))
    for x in [-4,-1,2]:
        b.collider("lounge-chair",(x,.65,4),(1.35,1.3,2.4))
        b.box((x,.4,4),(1.3,.15,2.3),'cream');b.box((x,.75,3.25),(1.3,.9,.15),'teal',rot=(-.3,0,0))

def backroads(b):
    building(b,-3,-4,5,4,3,'stone')
    for x,z in [(-1,1.2),(1.3,1),(2.8,-.5)]:bicycle(b,x,z)
    b.collider("van",(3,1.3,-4),(2.6,2.6,4.2))
    # Travel van with roof luggage, framed windows and wheels.
    b.box((3,1.2,-4),(2.3,1.8,4),'cream');b.box((3,.7,-4),(2.35,.65,4.05),'teal')
    b.box((3,1.65,-1.95),(1.9,.8,.05),'glass')
    for side in [-1,1]:
        for z in [-5.3,-2.7]:b.ball((3+side*1.1,.5,z),(.2,.45,.45),'iron');b.ball((3+side*1.28,.5,z),(.04,.23,.23),'brass')
        for z in [-4.8,-3.3]:b.box((3+side*1.17,1.55,z),(.04,.7,1),'glass')
    b.box((3,2.2,-4),(2.5,.16,4.2),'oak');crate(b,2.5,2.3,-4,.7);crate(b,3.5,2.3,-4.5,.8)
    for z in [2.8,4.5]:
        b.collider("workbench",(-2,.8,z),(2.6,1.6,.85))
        b.box((-2,.8,z),(2.6,.14,.85),'oak')
        for x in [-3,-1]:b.beam((x,0,z),(x,.8,z),.06,'iron')

def learning(b):
    building(b,-2,-4,5.5,4,3,'stone')
    desk(b,-1,1)
    for side in [-1,1]:
        x=side*3
        b.collider("bookcase",(x+side*.6,1.4,0),(1.5,2.8,1.5))
        b.box((x,1.4,0),(.2,2.8,1.5),'darkwood')
        for y in [.25,1,1.75,2.5]:
            b.box((x+side*.6,y,0),(1.3,.12,1.5),'wood')
            for k in range(6):b.box((x+side*.6,y+.3,-.5+k*.2),(.7,.5,.15),['red','teal','cream'][k%3])
    b.collider("reading-table",(2,.9,3),(2,1.8,1.2))
    b.box((2,.9,3),(2,.14,1.2),'oak');b.box((2,1.05,3),(1.1,.06,.75),'cream',rot=(0,.15,0))

def oclock(b):
    building(b,-2,-4,7,4,3.4,'stone')
    # Clock facade, classroom tables and a communal learning board.
    b.ring((-2,3.6,-1.88),.65,.08,'brass','z');b.ball((-2,3.6,-1.91),(.58,.58,.04),'cream')
    moving_part(b,"clock-minute",(-2,3.6,-1.82),lambda p:p.beam((-2,3.6,-1.82),(-2,4.03,-1.82),.025,"iron"))
    moving_part(b,"clock-hour",(-2,3.6,-1.82),lambda p:p.beam((-2,3.6,-1.82),(-1.7,3.5,-1.82),.025,"iron"))
    for x in [-3,0,3]: desk(b,x,1.3)
    b.collider("board",(4,1.5,-2),(2.6,3,.25))
    b.box((4,1.8,-2),(2.5,1.7,.12),'darkwood');b.box((4,1.8,-1.92),(2.3,1.5,.04),'teal')
    for i in range(5):b.box((3.4+(i%2)*.5,2.2-(i//2)*.3,-1.88),(.6,.04,.02),'cream')

def build_chapter(name):
    index=CHAPTERS.index(name);b=Batch(name);base(b,13,index+12)
    {'atelier':pavilion,'warehouse':warehouse,'masonry':masonry,'farm':farm,'clubmed':clubmed,'circus':circus,'backroads':backroads,'learning':learning,'oclock':oclock}[name](b)
    for x in [-7,6]:
        b.beam((x,0,2),(x,4,2),.075,"wood")
        b.collider("bunting-post",(x,2,2),(.2,4,.2),"cylinder")
    bunting(b,(-7,4,2),(6,4,2))
    objects=b.finish()+b.parts
    layout_path=ROOT/"src/features/journey/layouts.json"
    layouts=json.loads(layout_path.read_text()) if layout_path.exists() else {}
    layouts[name]=b.colliders
    layout_path.write_text(json.dumps(layouts,indent=2)+"\n")
    export(objects,OUT/(name+'.glb'))
    for o in objects:o.hide_set(True);o.hide_render=True
    return {'chapter':name,'meshes':len(objects),'faces':sum(len(o.data.polygons) for o in objects if o.type=="MESH")}
