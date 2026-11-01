"""Smooth profile surfaces and tapered curved forms for the hero-scale cast."""
import math
import bpy
from mathutils import Vector, Matrix
from craft import Batch, MATS, material


def catmull(points, steps=5):
    import numpy as np
    points=[np.array(p,dtype=float) for p in points]
    result=[]
    for i in range(len(points)-1):
        a,b,c,d=points[max(0,i-1)],points[i],points[i+1],points[min(len(points)-1,i+2)]
        for j in range(steps):
            t=j/steps
            result.append((2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)*.5)
    return [Vector(p) if len(p)==3 else tuple(p) for p in result+[points[-1]]]


class Organic(Batch):
    def ball(self,p,s,mat='skin',rot=None,segments=24,rings=16):
        vertices=[]
        rotation=Matrix.Rotation(rot[1],3,'Y')@Matrix.Rotation(rot[0],3,'X')@Matrix.Rotation(rot[2],3,'Z') if rot else Matrix.Identity(3)
        for j in range(rings+1):
            phi=math.pi*j/rings
            for i in range(segments):
                a=math.tau*i/segments
                v=Vector((math.sin(phi)*math.cos(a)*s[0],math.cos(phi)*s[1],math.sin(phi)*math.sin(a)*s[2]))
                vertices.append(rotation@v+Vector(p))
        faces=[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(rings) for i in range(segments)]
        self.mesh(vertices,faces,mat,True)

    def profile(self,rows,mat,segments=32,steps=4):
        """Rows: height, x center, z center, width radius, depth radius."""
        rows=catmull(rows,steps); verts=[]
        for y,x,z,rx,rz in rows:
            for i in range(segments):
                a=i*math.tau/segments
                verts.append((x+max(.001,rx)*math.cos(a),y,z+max(.001,rz)*math.sin(a)))
        faces=[(j*segments+i,(j+1)*segments+i,(j+1)*segments+(i+1)%segments,j*segments+(i+1)%segments) for j in range(len(rows)-1) for i in range(segments)]
        faces.extend([tuple(range(segments)),tuple(range(len(rows)*segments-1,(len(rows)-1)*segments-1,-1))])
        self.mesh(verts,faces,mat,True)

    def curve(self,points,radius,mat,sides=8,steps=4,taper=0):
        points=catmull(points,steps); verts=[]
        for i,p in enumerate(points):
            tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
            side=tangent.cross(Vector((0,0,1)))
            if side.length<.01: side=tangent.cross(Vector((1,0,0)))
            side.normalize(); up=tangent.cross(side)
            t=i/(len(points)-1)
            r=radius*(max(.06,math.sin(math.pi*t))**taper if taper else 1)
            for j in range(sides):
                a=math.tau*j/sides; verts.append(p+r*(math.cos(a)*side+math.sin(a)*up))
        faces=[(i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j) for i in range(len(points)-1) for j in range(sides)]
        faces.extend([tuple(range(sides-1,-1,-1)),tuple(range((len(points)-1)*sides,len(points)*sides))])
        self.mesh(verts,faces,mat,True)


def detail_palette():
    specs={
        'skinDetail':('#ce9c7b',.64,None),'skinRose':('#b97962',.7,None),
        'lip':('#945947',.72,None),'iris':('#6e815a',.36,None),
        'sclera':('#f2e9d8',.38,None),'hairDetail':('#493126',.67,None),
        'hairLight':('#6d4931',.7,None),'stitch':('#d5b78b',.9,None),
        'shirt':('#e5d8b9',.86,'cloth'),'coatDetail':('#397572',.82,'cloth'),
        'leatherDetail':('#795037',.72,'stone'),'leatherEdge':('#a1744b',.8,None),
        'wool':('#e6dac3',.96,'stone'),'woolLight':('#f3e9d6',.97,'stone'),
        'woolShade':('#ddd1bb',.96,'stone'),'animalSkin':('#5b5146',.88,None),
        'hoof':('#312e2a',.8,None),'earInner':('#a67f70',.92,None),
    }
    for name,(color,rough,tex) in specs.items(): material(name,color,rough=rough,texture=tex)
    # Packed normal maps survive glTF export; no Blender-only procedural nodes.
    import numpy as np
    for name in ['shirt','coatDetail','leatherDetail']:
        m=MATS[name]; nodes=m.node_tree.nodes
        if any(n.type=='NORMAL_MAP' for n in nodes):continue
        n=128; yy,xx=np.mgrid[0:n,0:n]
        if name in ['shirt','coatDetail']:
            height=np.sin(xx*math.tau/8)*np.sin(yy*math.tau/8)*.55
        else:
            rng=np.random.default_rng(17);height=rng.random((n,n))*.65
        dx=np.roll(height,-1,1)-np.roll(height,1,1);dy=np.roll(height,-1,0)-np.roll(height,1,0)
        normal=np.stack([-dx,-dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=2)[...,None]
        pixels=np.ones((n,n,4),dtype=np.float32);pixels[:,:,:3]=normal*.5+.5
        img=bpy.data.images.new('TEX-detail-normal-'+name,width=n,height=n,alpha=False)
        img.colorspace_settings.name='Non-Color';img.pixels.foreach_set(pixels.ravel());img.pack()
        tex=nodes.new('ShaderNodeTexImage');tex.image=img
        normal_node=nodes.new('ShaderNodeNormalMap');normal_node.inputs['Strength'].default_value=.28
        shader=next(n for n in nodes if n.type=='BSDF_PRINCIPLED')
        m.node_tree.links.new(tex.outputs['Color'],normal_node.inputs['Color'])
        m.node_tree.links.new(normal_node.outputs['Normal'],shader.inputs['Normal'])
