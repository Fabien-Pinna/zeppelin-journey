"""Career dioramas. Import craft first; call build_chapter per bounded MCP task."""
import bpy, math, random, json
from mathutils import Vector
from craft import Batch, base, building, bunting, tree, flowerbed, lantern, crate, barrel, bicycle, export, OUT, ROOT, moving_part
from animals import sheep
from landscapes import provence, mediterranean, circus_backstage

CHAPTERS=['atelier','warehouse','masonry','farm','clubmed','circus','backroads','learning','oclock']

def desk(b,x,z):
    b.collider("desk",(x,.85,z),(2,1.7,.8))
    b.collider("chair",(x,.65,z+1),(.7,1.3,.75))
    b.box((x,.85,z),(2,.14,.8),'oak')
    for dx in [-.85,.85]:
        for dz in [-.28,.28]: b.beam((x+dx,0,z+dz),(x+dx,.83,z+dz),.045,'iron')
    b.box((x,1.35,z-.2),(1,.65,.07),'iron');b.box((x,1.35,z-.155),(.89,.53,.02),'display')
    b.box((x-.33,1.35,z-.14),(.16,.48,.008),'teal')
    for row in range(7):
        length=.20+((row*7)%5)*.055
        b.box((x-.13+length/2,1.55-row*.055,z-.139),(length,.012,.006),'pixelGold' if row%3==0 else 'pixelBlue')
    b.box((x,.96,z+.15),(.75,.035,.25),'cream')
    b.beam((x,1,z-.2),(x,1.25,z-.2),.035,'iron')
    b.box((x,.5,z+1),(.65,.13,.65),'leather');b.box((x,.94,z+1.3),(.65,.8,.1),'teal')
    for dx in [-.22,.22]: b.beam((x+dx,0,z+.8),(x+dx,.5,z+1),.04,'iron')

def pavilion(b):
    from scenic_craft import pavilion as authored
    return authored(b)


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

def circus(b):
    from scenic_craft import circus as authored
    return authored(b)


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
    index=CHAPTERS.index(name);b=Batch(name)
    landscape=json.loads((ROOT/'src/features/journey/landscapes.json').read_text())[name]
    base(b,13,index+12,landscape)
    {'atelier':pavilion,'warehouse':warehouse,'masonry':masonry,'farm':provence,'clubmed':mediterranean,'circus':circus,'backroads':backroads,'learning':learning,'oclock':oclock}[name](b)
    if name=='circus':circus_backstage(b)
    if name not in ['farm','clubmed','circus']:
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
