"""Eroded limestone cliffs and peripheral gardens following the gameplay boundary exactly."""
import math
import random
from botany import fern, grass, ivy, flowers


def boundary(shape,a):
    return (abs(math.cos(a)/shape['rx'])**shape['power']+abs(math.sin(a)/shape['rz'])**shape['power'])**(-1/shape['power'])*(1+shape['scallop']*math.cos(3*a+shape['phase']))


def island_ground(b,shape,seed):
    rng=random.Random(seed)
    n=160;rows=32;depth=shape['depth']
    verts=[]
    for row in range(rows+1):
        t=row/rows
        for i in range(n):
            a=i*math.tau/n
            taper=(1-t)**.47
            # Continuous vertical fluting and ledges, not independently scattered boulders.
            flute=(.055*math.sin(a*17+seed)+.032*math.sin(a*31+1)+.018*math.cos(a*49))*math.sin(math.pi*t)**.55
            shelf=.022*math.sin(t*math.pi*11+a*.7)*math.sin(math.pi*t)
            radius=boundary(shape,a)*(taper+flute+shelf)
            y=-depth*t + math.sin(math.pi*t)*.22*math.sin(a*13+seed)
            verts.append((math.cos(a)*radius,y,math.sin(a)*radius))
    b.mesh(verts,[tuple(range(n-1,-1,-1))],shape['ground'])
    bands={'cliff':[],'cliffWarm':[],'cliffShade':[]}
    for row in range(rows):
        for i in range(n):
            a=i*math.tau/n
            band='cliffWarm' if row<2 or (row%9==3 and math.sin(a*3)>.1) else 'cliffShade' if math.sin(a*17+seed)<-.7 else 'cliff'
            bands[band].append((row*n+i,row*n+(i+1)%n,(row+1)*n+(i+1)%n,(row+1)*n+i))
    for mat,faces in bands.items():b.mesh(verts,faces,mat,True)
    # Small irregular sedimentary rim stones give a tangible edge at walking scale.
    for i in range(48):
        a=i*math.tau/48+rng.uniform(-.03,.03);r=boundary(shape,a)-rng.uniform(.12,.5)
        if shape['style']=='coast' and math.cos(a)*r < -13.4:continue
        b.shape('rock',(math.cos(a)*r,-.17,math.sin(a)*r),(.35+rng.random()*.30,.18+rng.random()*.15,.24+rng.random()*.22),'stoneLight' if i%3 else 'stone',rot=(0,-a,0))


def rim_gardens(b,shape,seed):
    rng=random.Random(seed+903)
    for i in range(220):
        a=rng.uniform(0,math.tau)
        r=boundary(shape,a)-rng.uniform(.45,2.0)
        x,z=math.cos(a)*r,math.sin(a)*r
        if x>4 and z>2:continue
        if shape['style']=='coast' and x<-5:continue
        if shape['style']=='industrial' and i%4:continue
        grass(b,x,z,rng.uniform(.7,1.5),seed*500+i)
        if i%8==0:fern(b,x,.02,z,rng.uniform(.5,1.1),seed+i)
        if i%17==0:flowers(b,x,z,.55,seed*31+i)
    for i in range(30):
        a=i*math.tau/30+.1
        r=boundary(shape,a)-.04
        x,z=math.cos(a)*r,math.sin(a)*r
        if x>4 and z>2:continue
        if shape['style']=='coast' and x<-13:continue
        if shape['style']=='industrial' and i%4:continue
        ivy(b,x,-.12,z,rng.uniform(1.6,4.8),seed*31+i)
