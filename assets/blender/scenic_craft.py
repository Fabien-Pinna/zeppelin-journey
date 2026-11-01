"""Reference-led scenery construction, sharing the original semantic collision contract."""
import math
import random
from mathutils import Vector
import botany
from terrain import island_ground, rim_gardens
from craft import lantern, crate, barrel, bunting


def tree(b,x,z,scale=1,seed=1):
    b.collider('tree',(x,1.8*scale,z),(.55*scale,3.6*scale,.55*scale),'cylinder')
    botany.tree(b,x,z,scale,seed)


def flowerbed(b,x,z,radius=1,seed=1):
    botany.flowers(b,x,z,radius,seed)


def paving_stone(b,x,z,w,d,seed,mat):
    rng=random.Random(seed)
    outline=[(-.5,-.32),(-.32,-.5),(.32,-.5),(.5,-.32),(.5,.32),(.32,.5),(-.32,.5),(-.5,.32)]
    outline=[(a+rng.uniform(-.055,.055),c+rng.uniform(-.055,.055)) for a,c in outline]
    verts=[(x+a*w*scale,y,z+c*d*scale) for y,scale in [(-.025,.88),(.025,1),(.075,.91)] for a,c in outline]
    b.mesh(verts,[(j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for j in range(2) for i in range(8)],mat,True)
    b.mesh(verts,[tuple(range(23,15,-1))],mat)


def dock(b):
    rng=random.Random(21)
    # Staggered timber boards with seams, grain, pegs and substantial supporting carpentry.
    for row in range(20):
        z=2.5+row*.37
        split=(-.8 if row%2 else .7)
        for x0,x1 in [(-2.1,split),(split,2.1)]:
            b.box((7+(x0+x1)/2,.08+rng.uniform(-.007,.007),z),(x1-x0-.025,.2,.345),'oak' if row%5 else 'wood')
            for x in [7+x0+.12,7+x1-.12]:
                for dz in [-.095,.095]:b.ball((x,.185,z+dz),(.014,.009,.014),'iron')
    for x in [5.2,8.8]:
        b.beam((x,-.35,2.2),(x,-.35,9.8),.17,'darkwood',12)
        for z in [3,6,9]:
            b.beam((x,-3,z),(x,.1,z),.15,'wood',12)
            b.beam((x,-2.3,z),(x,-.3,z+1),.1,'wood',12)
    for side in [-1,1]:
        x=7+side*2.2
        for z in [2.5,5,7.5,9.5]:
            b.beam((x,-2,z),(x,1.05,z),.12,'darkwood',12)
            b.ring((x,.95,z),.13,.025,'brass')
            b.ball((x,1.09,z),(.16,.12,.16),'brass')
            b.collider('pier-post',(x,.6,z),(.3,1.3,.3),'cylinder')
        for height in [.48,.95]:
            for a,c in [(2.5,5),(5,7.5),(7.5,9.5)]:
                points=[(x,height-.14*math.sin(t*math.pi),a+(c-a)*t) for t in [i/12 for i in range(13)]]
                botany.stem(b,points,.025,'oak',6)
    lantern(b,4.8,9.3);lantern(b,9.2,9.3)
    crate(b,8.5,.2,3.3);barrel(b,5.5,3.2,.8)
    for i in range(4):b.ring((8.6,.22+i*.022,8.5),.35-i*.055,.018,'cream')


def base(b,r=13,seed=1,landscape=None):
    shape=landscape or {'rx':r,'rz':r,'power':2,'scallop':.03,'phase':0,'depth':9,'style':'garden','path':'stone','ground':'grass'}
    rng=random.Random(seed)
    island_ground(b,shape,seed)
    rim_gardens(b,shape,seed)
    if shape['path']=='stone':
        for j in range(7):
            for i in range(7):
                x=(i-3)*.8+math.sin(j)*.15;z=(j-1)*.8
                paving_stone(b,x,z,.77,.75,seed*100+i*7+j,rng.choice(['stone','stoneLight']))
                if (i+j)%6==0:botany.grass(b,x+.4,z,.3,i*80+j,y=.02)
    elif shape['path']=='carpet':
        b.box((1,.025,3),(2,.06,6),'red')
        for x in [.04,1.96]:b.box((x,.06,3),(.035,.009,6),'brass')
    elif shape['path']=='yard':
        for i in range(6):b.box((i-3,.025,4),(.85,.06,3.8),'yard')
    elif shape['path']=='earth':
        # Thin irregular patches settle into the surface instead of looking like floating blobs.
        for i in range(9):b.ball((4-i*.65,-.012,5-i*.45),(1,.028,.6),'soil')
    for i in range(7):b.box((2.8+i*.6,.04,4.6),(.58,.09,1.1),'oak' if shape['path']=='sand' else 'stone')
    dock(b)
    if shape['style'] not in ['orchard','coast','circus','industrial']:
        for i,(x,z,s) in enumerate([(-8,-4,1.2),(6,-7,1.3),(-9,4,.8),(8,0,.9)]):tree(b,x,z,s,seed*10+i)
    for x,z in [(-10,7),(10,1),(-7,-1),(9,-5.5)]:
        if shape['style'] in ['coast','circus']:continue
        if shape['style']=='orchard' and x<0:continue
        lantern(b,x,z)
    if shape['style'] in ['garden','trail','campus']:
        for side in [-1,1]:
            for j in range(5):
                x=side*(7+j%2*1.5);z=-8+j*2.4
                flowerbed(b,x,z,.85,seed*500+j)
                botany.fern(b,x+.6,.02,z+.25,.9,seed+j)
    if b.name=='atelier':
        # Lush shoulder gardens frame the walk; the guide and boarding approach stay open.
        for i,(x,z) in enumerate([(-4.3,1.3),(-4.5,3.2),(-3.5,5.5),(-1.8,6.8),(.2,7.0),(4.7,1.4),(5.1,-1.3)]):
            flowerbed(b,x,z,.85,seed*73+i)
            botany.fern(b,x-.3,.02,z+.3,1.05,seed+i)
            for k in range(8):botany.grass(b,x+rng.uniform(-1,1),z+rng.uniform(-.8,.8),1,seed*60+i*8+k)


def tile(b,center,width,length,slope,mat):
    # Curved terracotta channel with an overlapping lip, not a beveled rectangular slab.
    x,y,z=center;verts=[];segments=8
    for v in [0,1]:
        for i in range(segments+1):
            a=math.pi*i/segments
            dx=(v-.5)*length
            dz=math.cos(a)*width*.5
            dy=math.sin(a)*width*.24+.02*v
            verts.append((x+dx*math.cos(slope)-dy*math.sin(slope),y+dx*math.sin(slope)+dy*math.cos(slope),z+dz))
    b.mesh(verts,[(i,i+1,segments+2+i,segments+1+i) for i in range(segments)],mat,True)


def building(b,x,z,w=5,d=4,h=3,wall='stone',roof='tile'):
    rng=random.Random(int((x+z)*27))
    b.collider('building',(x,h/2,z),(w,h,d))
    b.box((x,h/2,z),(w,h,d),'plaster' if wall=='stone' else wall)
    for row in range(int(h/.38)):
        for col in range(int(w/.62)):
            px=x-w/2+.30+col*.62+(row%2)*.15
            if abs(px-x)<.6 and row<5:continue
            b.box((px,.20+row*.38,z+d/2+.04),(.58+rng.uniform(-.04,.03),.34+rng.uniform(-.02,.02),.17),rng.choice(['stoneLight','stone','cliffWarm']),rot=(0,0,rng.uniform(-.025,.025)))
    for side in [-1,1]:
        for row in range(int(h/.42)):
            b.box((x+side*(w/2-.04),.22+row*.42,z+d/2),(.45,.38,.48),'stoneLight')
        wx=x+side*w*.29
        b.box((wx,1.8,z+d/2+.16),(1,1.2,.1),'darkwood')
        b.box((wx,1.8,z+d/2+.22),(.78,.99,.04),'lamp')
        for shift in [-.2,.2]:b.box((wx+shift,1.8,z+d/2+.27),(.035,1.02,.05),'wood')
        for yy in [1.56,1.98]:b.box((wx,yy,z+d/2+.27),(.84,.035,.05),'wood')
        b.box((wx,1.12,z+d/2+.3),(1.2,.12,.4),'wood')
        for ss in [-1,1]:
            b.box((wx+ss*.7,1.8,z+d/2+.19),(.42,1.2,.09),'teal')
            for j in range(8):b.box((wx+ss*.7,1.3+j*.14,z+d/2+.25),(.39,.035,.025),'wood')
        b.box((wx,1.20,z+d/2+.37),(1.05,.18,.3),'tile')
        for j in range(9):
            px=wx-.45+j*.11
            for k in range(3):botany.leaf(b,(px,1.3,z+d/2+.38),.19,.07,k*2.4,.5,'leaf')
            for k in range(5):botany.leaf(b,(px,1.53,z+d/2+.38),.055,.045,k*math.tau/5,.1,'rose')
    b.box((x,1.05,z+d/2+.14),(1.1,2.1,.16),'teal')
    for i in range(5):b.box((x-.43+i*.215,1.05,z+d/2+.24),(.018,2.0,.02),'darkwood')
    for yy in [.25,1.75]:b.box((x,yy,z+d/2+.26),(.95,.07,.03),'wood')
    b.ball((x+.35,1,z+d/2+.29),(.045,.045,.045),'brass')
    b.box((x,.06,z+d/2+.38),(1.4,.12,.55),'stoneLight')
    for side in [-1,1]:
        for row in range(8):
            xx=side*(row+.5)*(w/2+.4)/8;yy=h+1.65-abs(xx)*.58
            for col in range(math.ceil((d+.6)/.32)):
                zz=z-d/2-.3+col*.32
                tile(b,(x+xx,yy,zz),.34,(w/2+.4)/8+.08,-side*.52,roof if (row+col)%4 else 'tileLight')
        b.beam((x+side*(w/2+.4),h-.05,z-d/2-.35),(x+side*(w/2+.4),h-.05,z+d/2+.35),.075,'darkwood',12)
    b.beam((x,h+1.7,z-d/2-.45),(x,h+1.7,z+d/2+.45),.1,'tileLight',16)
    b.mesh([(x-w/2,h,z+d/2),(x+w/2,h,z+d/2),(x,h+1.65,z+d/2)],[(0,1,2)],'plaster')
    b.box((x+1.5,h+1.3,z-.7),(.65,1.8,.65),'brick')
    for j in range(5):b.box((x+1.5,h+.55+j*.34,z-.34),(.67,.025,.02),'stone')
    b.box((x+1.5,h+2.25,z-.7),(.85,.16,.85),'stone')
    botany.ivy(b,x-w/2-.03,h+.2,z+d/2+.2,h*.85,int(x*31+z))


def pavilion(b):
    from islands import desk
    # Open-front curved conservatory, preserving its footprint and usable studio interior.
    b.box((-2,.08,-3),(8,.22,6),'wood')
    for row in range(12):
        for col in range(3):b.box((-4.65+col*2.65,.21,-5.8+row*.47),(2.60,.08,.435),'oak' if (row+col)%4 else 'wood')
    for x in [-5.7,-2,1.7]:
        for z in [-5.7,-.3]:
            b.beam((x,.25,z),(x,3.8,z),.10,'teal',16)
            for y in [.32,3.7]:b.box((x,y,z),(.36,.18,.36),'brass')
    for x in [-5.7,1.7]:
        b.box((x,.65,-3),(.2,1.0,5.5),'stone')
        for z in [-4.8,-3.2,-1.6]:
            b.box((x,2.45,z),(.035,2.35,1.4),'glass')
            for y in [1.3,2.45,3.65]:b.beam((x,y,z-.74),(x,y,z+.74),.025,'teal',10)
            for zz in [z-.75,z+.75]:b.beam((x,1.25,zz),(x,3.7,zz),.035,'teal',10)
    b.box((-2,1,-5.8),(7.6,1.8,.17),'plaster')
    for x in [-4.4,-2,.4]:desk(b,x,-3.3)
    # Barrel-vault ribs and tinted curved panes. The front remains open for walking.
    segments=40
    def roof_point(t,z,offset=0):
        a=math.pi*t
        return (-2-4.0*math.cos(a),3.7+1.9*math.sin(a)+offset,z)
    for col in range(8):
        z0=-6.1+col*.9;z1=z0+.88
        vertices=[roof_point(i/segments,z) for z in [z0,z1] for i in range(segments+1)]
        b.mesh(vertices,[(i,i+1,segments+2+i,segments+1+i) for i in range(segments)],'glass',True)
    for j in range(9):botany.stem(b,[roof_point(i/segments,-6.12+j*.9,.025) for i in range(segments+1)],.055,'teal',10)
    for i in range(9):
        p=roof_point(i/8,-6.2,.04);q=roof_point(i/8,1.1,.04)
        b.beam(p,q,.035,'brass',10)
    for x in [-5.8,1.8]:lantern(b,x,-.1,3.1)
    for x in [-5.7,1.7]:b.collider('pavilion-wall',(x,2,-3),(.28,4,5.5))
    b.collider('pavilion-back',(-2,2,-5.8),(7.6,4,.25))
    for x in [-5.7,-2,1.7]:b.collider('pavilion-post',(x,2,-.3),(.3,4,.3),'cylinder')
    b.collider('display',(2.5,1.2,1),(1.3,2.4,.7))
    b.box((2.5,.8,1),(1.3,1.6,.7),'wood');b.box((2.5,1.9,1),(1.1,.85,.09),'iron');b.box((2.5,1.9,1.06),(.94,.7,.02),'display')
    # Fitted bookshelves and personal working clutter sit behind the desks, not on paths.
    for y in [.4,.95,1.5,2.05]:b.box((-2,y,-5.55),(7.1,.08,.32),'oak')
    rng=random.Random(45)
    for i in range(30):
        x=-5.35+(i%15)*.46;y=.45+(i//15)*1.05
        for k in range(3):b.box((x+k*.12,y+.18,-5.5),(.09,.30+rng.uniform(0,.13),.22),rng.choice(['red','teal','cream','leather']))
    for x in [-4.4,-2,.4]:
        b.ring((x+.7,1.02,-3.15),.09,.018,'cream')
        b.beam((x+.7,.94,-3.15),(x+.7,1.1,-3.15),.07,'cream',16)
        b.box((x-.65,.95,-3.25),(.36,.035,.27),'red')
    for x in [-5.4,1.4]:
        b.box((x,.4,-.65),(.5,.65,.5),'tile')
        botany.fern(b,x,.73,-.65,1.25,int(x*20))
        botany.ivy(b,x,3.6,-.4,1.4,int(x*10))
    bunting(b,(-5.7,3.65,.5),(1.7,3.65,.5))


def circus(b):
    # Concave tensioned canvas with a scalloped valance and folds in the open side curtains.
    n=96;rows=14;r=4.3;verts=[]
    for j in range(rows+1):
        t=j/rows;rad=.12+(r-.12)*t
        for i in range(n):
            a=i*math.tau/n
            h=6-2.9*t**.55 + .055*math.cos(a*24)*math.sin(math.pi*t)
            verts.append((rad*math.cos(a),h,-3+rad*math.sin(a)))
    for color in ['red','cream']:
        faces=[]
        for j in range(rows):
            for i in range(n):
                if (i//4)%2==(0 if color=='red' else 1):faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
        b.mesh(verts,faces,color,True)
    for i in range(n):
        a=i*math.tau/n;c=(i+1)*math.tau/n;color='red' if (i//4)%2==0 else 'cream'
        b.mesh([(r*math.cos(a),3.12,-3+r*math.sin(a)),(r*math.cos(c),3.12,-3+r*math.sin(c)),(r*math.cos(c),2.86-.13*math.sin(c*12)**2,-3+r*math.sin(c)),(r*math.cos(a),2.86-.13*math.sin(a*12)**2,-3+r*math.sin(a))],[(0,1,2,3)],color,True)
        if math.sin(a)<.55:
            rad=r+.065*math.cos(a*48)
            rc=r+.065*math.cos(c*48)
            b.mesh([(rad*math.cos(a),0,-3+rad*math.sin(a)),(rc*math.cos(c),0,-3+rc*math.sin(c)),(r*math.cos(c),3.1,-3+r*math.sin(c)),(r*math.cos(a),3.1,-3+r*math.sin(a))],[(0,1,2,3)],color,True)
    # Original wall collider layout retained for navigation and performer clearances.
    for i in range(40):
        a=(i+.5)*math.tau/40
        if math.sin(i*math.tau/40)<.55:b.collider('tent-wall',(math.cos(a)*4.3,1.5,-3+math.sin(a)*4.3),(.72,3,.72),'cylinder')
    b.collider('tent-pole',(0,3.4,-3),(.2,6.8,.2),'cylinder')
    b.beam((0,0,-3),(0,6.8,-3),.07,'brass',16)
    b.mesh([(0,6.8,-3),(1.2,6.5,-3),(0,6.2,-3)],[(0,1,2)],'red')
    b.ring((0,.2,-3),3.8,.14,'brass',segments=80)
    b.ring((0,3.1,-3),4.3,.06,'brass',segments=96)
    for i in range(48):
        a=i*math.tau/48
        b.ball((math.cos(a)*4.32,2.85,-3+math.sin(a)*4.32),(.045,.06,.045),'lamp')
    for row in range(3):
        for col in range(8):
            x=-3+col*.85;z=3+row*.8
            b.collider('seat',(x,.65,z),(.65,1.3,.65))
            b.box((x,.5,z),(.65,.12,.6),'wood');b.box((x,.9,z+.27),(.65,.7,.09),'red')
            for dx in [-.23,.23]:b.beam((x+dx,0,z),(x+dx,.5,z),.035,'iron',10)
    for x in [-3.8,3.8]:lantern(b,x,1,2.8)
