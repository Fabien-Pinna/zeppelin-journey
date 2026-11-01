"""Anatomical sheep with layered fleece and independent grazing/leg pivots."""
import math
from craft import moving_part
from organic import Organic, detail_palette


def sheep(batch,x,z,s=1,identity='a'):
    detail_palette()
    b=Organic('sheep-'+identity)
    def p(a):return (x+a[0]*s,a[1]*s,z+a[2]*s)
    def ball(c,r,mat,**kw):b.ball(p(c),tuple(v*s for v in r),mat,**kw)
    ball((-.05,.78,0),(.57,.34,.32),'wool')
    # Fleece follows the torso, with overlapping varied curls, not a few balls.
    for i in range(340):
        u=1-2*(i+.5)/340;a=i*2.399963
        radial=math.sqrt(1-u*u)
        c=(-.05+.52*u,.79+.32*radial*math.cos(a),.30*radial*math.sin(a))
        size=.047+.018*(.5+.5*math.sin(i*7.1))
        ball(c,(size*1.3,size,size),'woolLight' if i%11==0 else 'woolShade' if i%7==0 else 'wool',segments=20,rings=12)
        if c[1]>.74 and i%3==0:
            points=[p((c[0]+size*.55*math.cos(j*math.tau/7),c[1]+size*.65+size*.14*math.sin(j),c[2]+size*.55*math.sin(j*math.tau/7))) for j in range(8)]
            b.curve(points,.006*s,'wool',6,2)
    b.curve([p((-.56,.84,0)),p((-.66,.72,.025)),p((-.68,.59,.015))],.07*s,'wool',10,taper=.3)
    # Transfer batched body surfaces into the island batch (coordinates are Blender Z-up here).
    def transfer(source,target):
        for mat,(verts,faces,smooth) in source.data.items():
            target.mesh([(a,c,-bb) for a,bb,c in verts],faces,mat,True)
    transfer(b,batch)
    def head(part):
        b=Organic('sheep-'+identity+'-head')
        b.curve([p((.36,.83,0)),p((.48,1.02,0)),p((.61,1.07,0))],.16*s,'animalSkin',14)
        b.ball(p((.59,1.08,0)),(.205*s,.20*s,.145*s),'animalSkin')
        b.ball(p((.75,.98,0)),(.19*s,.105*s,.12*s),'animalSkin')
        b.ball(p((.895,.97,0)),(.045*s,.055*s,.08*s),'hoof')
        for side in [-1,1]:
            b.ball(p((.48,1.14,side*.20)),(.15*s,.045*s,.075*s),'animalSkin',rot=(0,side*.35,side*.2))
            b.ball(p((.49,1.166,side*.205)),(.102*s,.012*s,.047*s),'earInner')
            b.ball(p((.65,1.115,side*.123)),(.038*s,.031*s,.024*s),'hoof')
            b.ball(p((.662,1.12,side*.141)),(.026*s,.022*s,.008*s),'iris')
            b.ball(p((.667,1.12,side*.149)),(.021*s,.006*s,.004*s),'eye')
            b.ball(p((.674,1.131,side*.153)),(.006*s,.006*s,.003*s),'sclera',segments=8,rings=6)
            b.ball(p((.897,1.0,side*.04)),(.015*s,.009*s,.012*s),'eye',segments=12,rings=8)
            b.curve([p((.9,.937,side*.025)),p((.82,.92,side*.078)),p((.75,.932,side*.10))],.007*s,'hoof',6)
        for i in range(15):
            a=i*2.4;r=.12*math.sqrt((i+.5)/15)
            b.ball(p((.53+math.cos(a)*r,1.24+.025*math.sin(i),math.sin(a)*r)),(.06*s,.048*s,.05*s),'wool',segments=20,rings=12)
        transfer(b,part)
    moving_part(batch,'sheep-'+identity+'-head',p((.36,.88,0)),head)
    for ix,dx in enumerate([-.36,.32]):
        for iz,dz in enumerate([-.20,.20]):
            def leg(part,dx=dx,dz=dz):
                b=Organic('sheep-leg')
                b.profile([(v*s,x+cx*s,z+cz*s,rx*s,rz*s) for v,cx,cz,rx,rz in [(.07,dx,dz,.065,.058),(.18,dx-.018,dz,.048,.046),(.32,dx+.018,dz,.047,.046),(.46,dx,dz,.064,.06),(.67,dx,dz,.085,.075)]],'animalSkin',16,3)
                for split in [-1,1]:b.ball(p((dx+.023,.065,dz+split*.031)),(.071*s,.067*s,.032*s),'hoof',segments=16,rings=10)
                transfer(b,part)
            moving_part(batch,f'sheep-{identity}-leg-{ix}{iz}',p((dx,.62,dz)),leg)
