"""Branching botanical silhouettes built from curved stems and individual folded leaves."""
import math
import random
from mathutils import Vector


def stem(b, points, radius, mat='darkwood', sides=8):
    verts, faces = [], []
    points = [Vector(p) for p in points]
    for i, p in enumerate(points):
        tangent = (points[min(i+1, len(points)-1)] - points[max(i-1, 0)]).normalized()
        right = tangent.cross(Vector((0, 0, 1)))
        if right.length < .01:
            right = tangent.cross(Vector((1, 0, 0)))
        right.normalize()
        up = tangent.cross(right)
        r = radius * (1 - .78 * i / (len(points)-1))
        for j in range(sides):
            a = j * math.tau / sides
            verts.append(p + (math.cos(a)*right + math.sin(a)*up) * r)
    for i in range(len(points)-1):
        for j in range(sides):
            faces.append((i*sides+j, i*sides+(j+1)%sides, (i+1)*sides+(j+1)%sides, (i+1)*sides+j))
    faces.extend([tuple(range(sides-1,-1,-1)), tuple(range((len(points)-1)*sides,len(points)*sides))])
    b.mesh(verts, faces, mat, True)


def leaf(b, p, length, width, angle, tilt, mat='leaf', curl=.12):
    p = Vector(p)
    forward = Vector((math.cos(angle)*math.cos(tilt), math.sin(tilt), math.sin(angle)*math.cos(tilt)))
    side = Vector((-math.sin(angle), 0, math.cos(angle)))
    # A convex, folded lens; opposed faces keep leaf backs visible in glTF.
    verts = [p, p + forward*length*.43 + side*width*.5,
             p + forward*length*.48 + Vector((0, length*curl, 0)),
             p + forward*length*.43 - side*width*.5, p + forward*length]
    faces = [(0,1,2), (1,4,2), (4,3,2), (3,0,2)]
    b.mesh(verts, faces + [tuple(reversed(f)) for f in faces], mat, True)


def canopy(b, center, radius, seed, kind='broad', count=520):
    rng = random.Random(seed)
    x,y,z = center
    mats = ['oliveDark','oliveLeaf','oliveLeaf'] if kind == 'olive' else ['leafDark','leaf','leaf','leafLight']
    for i in range(count):
        a = rng.uniform(0, math.tau)
        h = rng.uniform(-1, 1)
        radial = math.sqrt(1-h*h) * rng.uniform(.4, 1)
        p = (x+math.cos(a)*radial*radius[0], y+h*radius[1], z+math.sin(a)*radial*radius[2])
        direction = a+rng.uniform(-.8,.8)
        if kind == 'pine':
            length,width = rng.uniform(.16,.30), .035
        elif kind == 'olive':
            length,width = rng.uniform(.14,.26), .055
        else:
            length,width = rng.uniform(.16,.32), rng.uniform(.08,.16)
        leaf(b,p,length,width,direction,rng.uniform(-.6,.65),rng.choice(mats))
        if kind == 'cherry' and i%23 == 0:
            b.ball((p[0],p[1]-.1,p[2]),(.045,.05,.045),'cherry')


def tree(b, x, z, scale=1, seed=1, kind='broad'):
    rng = random.Random(seed)
    h = (4.1 if kind=='broad' else 3.3) * scale
    stem(b,[(x,0,z),(x-.13*scale,h*.24,z+.12*scale),(x+.17*scale,h*.6,z),(x+.05*scale,h*.91,z+.1*scale)],.24*scale,sides=12)
    for i in range(9):
        a = i*2.39996 + rng.uniform(-.2,.2)
        reach = rng.uniform(.9,1.65)*scale
        y = h*(.7+.28*(i%3)/2)
        end = (x+math.cos(a)*reach,y,z+math.sin(a)*reach)
        stem(b,[(x,h*.38,z),(x+math.cos(a)*reach*.35,y*.85,z+math.sin(a)*reach*.35),end],.095*scale)
        for j in range(3):
            angle = a+(j-1)*.8
            tip = (end[0]+math.cos(angle)*.65*scale,end[1]+.25*scale,end[2]+math.sin(angle)*.65*scale)
            stem(b,[end,((end[0]+tip[0])/2,end[1]+.25*scale,(end[2]+tip[2])/2),tip],.028*scale,'wood',6)
            canopy(b,tip,(.73*scale,.45*scale,.7*scale),seed*100+i*7+j,kind,140 if kind!='pine' else 210)
    for i in range(5):
        a=i*math.tau/5
        stem(b,[(x,.35*scale,z),(x+math.cos(a)*.35*scale,.1,z+math.sin(a)*.35*scale),(x+math.cos(a)*.7*scale,.025,z+math.sin(a)*.7*scale)],.1*scale)


def fern(b,x,y,z,s=1,seed=1):
    rng=random.Random(seed)
    for i in range(7):
        a=i*2.4
        points=[(x,y,z),(x+math.cos(a)*.25*s,y+.45*s,z+math.sin(a)*.25*s),(x+math.cos(a)*.6*s,y+.35*s,z+math.sin(a)*.6*s)]
        stem(b,points,.012*s,'leafDark',5)
        for k in range(6):
            t=(k+1)/7
            p=(x+math.cos(a)*t*.6*s,y+math.sin(t*math.pi*.8)*.45*s,z+math.sin(a)*t*.6*s)
            for side in [-1,1]:
                leaf(b,p,(.24-.15*t)*s,.045*s,a+side*1.05,.1,rng.choice(['leaf','leafLight']))


def grass(b,x,z,s=1,seed=1,y=0):
    rng=random.Random(seed)
    for i in range(8):
        a=rng.uniform(0,math.tau)
        h=rng.uniform(.12,.34)*s
        px=x+rng.uniform(-.12,.12)*s;pz=z+rng.uniform(-.12,.12)*s
        leaf(b,(px,y,pz),h,.016*s,a,rng.uniform(.75,1.4),rng.choice(['leaf','leafLight','meadow']),.15)


def flowers(b,x,z,radius=1,seed=1):
    rng=random.Random(seed)
    for i in range(48):
        a=rng.uniform(0,math.tau);r=math.sqrt(rng.random())*radius
        px=x+math.cos(a)*r;pz=z+math.sin(a)*r;h=rng.uniform(.18,.58)
        stem(b,[(px,.015,pz),(px+.025,h*.6,pz),(px+.06,h,pz+.03)],.009,'leafDark',5)
        for j in range(3):
            leaf(b,(px+.02,h*(.18+j*.21),pz),.15,.055,a+j*2.4,.3,'leaf')
        mat=['purple','white','flower','rose'][i%4]
        for j in range(5):
            leaf(b,(px+.06,h,pz+.03),.065,.06,j*math.tau/5,.2,mat,.3)
        b.ball((px+.06,h+.02,pz+.03),(.026,.022,.026),'flower')
        if i%4==0:grass(b,px,pz,.8,seed+i)


def ivy(b,x,y,z,length,seed):
    rng=random.Random(seed)
    for strand in range(3):
        a=rng.uniform(0,math.tau)
        points=[]
        for k in range(14):
            t=k/13
            p=(x+strand*.13+math.sin(t*8+strand)*.15,y-t*length,z+math.cos(t*9+strand)*.16)
            points.append(p)
            if k:
                for side in [-1,1]:leaf(b,p,.18*(1-.4*t),.14,a+side*.8,rng.uniform(-.6,.3),'leaf' if k%3 else 'leafLight')
        stem(b,points,.015,'darkwood',5)
