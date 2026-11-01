"""Distinct, authored places; source facts and reference geometry in ASSETS.md."""
import bpy, math, random, json
import botany
from mathutils import Matrix, Vector
from craft import Batch, ROOT, building, crate, barrel, tree, lantern, moving_part, material, MATS
from organic import Organic, detail_palette
from animals import sheep

def transfer(source,target):
    for mat,(verts,faces,smooth) in source.data.items():
        target.mesh([(x,z,-y) for x,y,z in verts],faces,mat,True)

def sign(b,text,x,y,z,width=4,color='cream',posts=False):
    b.box((x,y,z),(width,.65,.13),'darkwood')
    if posts:
        for dx in [-width*.38,width*.38]:
            b.beam((x+dx,0,z),(x+dx,y-.3,z),.045,'wood')
            b.collider('sign-post',(x+dx,y/2,z),(.12,y,.12),'cylinder')
    curve=bpy.data.curves.new('sign-'+text,'FONT');curve.body=text;curve.align_x='CENTER';curve.align_y='CENTER';curve.size=.34;curve.extrude=.004
    obj=bpy.data.objects.new('GEO-sign-'+text,curve);bpy.context.scene.collection.objects.link(obj)
    obj.location=(x,-z-.09,y);obj.rotation_euler=(math.pi/2,0,0);curve.materials.append(MATS[color])
    bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.convert(target='MESH');obj.select_set(False);b.parts.append(obj)

def orchard_tree(b,x,z,kind,seed,s=1):
    import botany
    botany.tree(b,x,z,s,seed,kind)
    b.collider(kind+'-trunk',(x,2.9*s/2,z),(.5*s,2.9*s,.5*s),'cylinder')


def dry_wall(b,x,z,length):
    rng=random.Random(int(x*13+z*5))
    for row in range(3):
        for col in range(int(length/.4)):
            b.shape('rock',(x-length/2+col*.4+row%2*.17,.13+row*.21,z),(.23,.13,.19),'stoneLight' if col%3 else 'stone',rot=(0,rng.random(),0))
    b.collider('dry-stone-wall',(x,.34,z),(length,.68,.4))

def provence(b):
    # The limestone ridge is a miniature evocation of the Ventoux, behind cultivated land.
    material('ventouxLimestone','#e0d8c9',rough=.98,texture='stone')
    verts=[];nx=72;nz=24
    for j in range(nz+1):
        v=j/nz;z=-12.2+v*4.4
        for i in range(nx+1):
            x=-9+18*i/nx
            h=.05+4.4*math.exp(-((x-.5)/5.8)**4)*math.sin(math.pi*v)**.75
            h+=math.sin(math.pi*v)*(.08*math.sin(x*3+z*2)+.04*math.sin(x*8-z*4))
            verts.append((x,h,z))
    low=[];high=[]
    for j in range(nz):
        for i in range(nx):
            a=j*(nx+1)+i;c=a+nx+1
            for face in [(a,c,a+1),(a+1,c,c+1)]:
                (high if sum(verts[k][1] for k in face)/3>2.65 else low).append(face)
    b.mesh(verts,low,'rockLight',True);b.mesh(verts,high,'ventouxLimestone',True)
    b.collider('ventoux-ridge',(0,2.2,-10),(17,5,4))
    building(b,5,-5.5,4,3.2,2.4,'stone')
    sign(b,'VAUCLUSE · MONT VENTOUX',5,3.1,-3.7,5.8)
    barrel(b,7.5,0,-3);crate(b,7.2,0,-1.3,.8)
    # Vine rows have trunks, wires, trained branches, leaves and grape bunches.
    o=Organic('vineyard')
    for row in range(4):
        z=-5+row*2.1
        b.box((-8,.05,z),(8,.13,.75),'soil')
        for x in [-12,-8,-4]:b.beam((x,0,z),(x,1.65,z),.055,'wood')
        for y in [.85,1.45]:b.beam((-12,y,z),(-4,y,z),.012,'iron',5)
        b.collider('vine-row',(-8,.8,z),(8.1,1.6,.8))
        for col in range(9):
            x=-11.7+col*.91
            o.curve([(x,0,z),(x+.1,.5,z),(x-.06,1.1,z),(x+.25,1.4,z)],.045,'darkwood',8)
            for i in range(10):
                a=i*2.4;p=(x+math.cos(a)*.44,1.25+math.sin(i)*.19,z+math.sin(a)*.29)
                botany.leaf(o,p,.30,.21,a,.2,'leafLight' if i%3 else 'leaf')
            for side in [-1,1]:
                for k in range(10):
                    a=k*2.4;rr=.065*(1-k/14)
                    o.ball((x+side*.23+math.cos(a)*rr,1.12-k*.021,z+.23+math.sin(a)*rr),(.042,.047,.042),'grape',segments=8,rings=6)
    transfer(o,b)
    dry_wall(b,-8,3,8.5)
    for i,(x,z) in enumerate([(-11,6),(-7.5,6.5),(-3.8,7.7)]):orchard_tree(b,x,z,'cherry',80+i,.9)
    for i,(x,z) in enumerate([(10,-6),(12,-2),(11,2),(-2,-5)]):orchard_tree(b,x,z,'olive',90+i,1.05)
    for x,z in [(-5,5),(-4,5),(-2,4.8)]:
        crate(b,x,0,z,.65)
        for i in range(12):b.ball((x-.22+(i%4)*.14,.58,z-.18+(i//4)*.14),(.075,.07,.075),'cherry')
    sign(b,'VIGNES · CERISIERS · OLIVIERS',-6,2.2,4.3,6,posts=True)
    moving_part(b,'sheep-a',(2,0,2),lambda part:sheep(part,2,2))
    moving_part(b,'sheep-b',(3.8,0,3),lambda part:sheep(part,3.8,3,.8,'b'))

def imported_rig(b):
    path=ROOT/'assets/blender/references/trapeze_rig_01.glb'
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));objects=list(set(bpy.data.objects)-before)
    bpy.context.view_layer.update()
    transform=Matrix.Translation((-4.3,1,0))@Matrix.Rotation(-math.pi/2,4,'Z')@Matrix.Scale(16,4)
    matrices={obj:obj.matrix_world.copy() for obj in objects}
    for obj in objects:
        if 'swing_fly' in obj.name or 'swing_catch' in obj.name:
            bpy.data.objects.remove(obj,do_unlink=True);continue
        obj.parent=None;obj.matrix_world=transform@matrices[obj]
        b.parts.append(obj)
    # Dimensions from the CATS / Caravan Atlas source, same transform as the mesh.
    for z,h in [(-6.456,6.544),(.088,6.832),(6.312,7.424)]:
        for x in [-7.212,-1.388]:b.collider('trapeze-post',(x,h/2,z),(.17,h,.17),'cylinder')
        for x in [-13.02,4.42]:b.collider('rig-anchor',(x,.2,z),(.28,.4,.28),'cylinder')
    b.collider('safety-net',(-4.3,2.032,-1.8),(5.824,.12,15.04))
    b.collider('departure-ladder',(-4.6,2.6,6.312),(1.3,5.2,.8))
    for z in [-13.48,11.48]:
        for x in [-8.78,.18]:b.collider('rig-anchor',(x,.4,z),(.4,.8,.4),'cylinder')

def pine(b,x,z,s=1):
    import botany
    botany.tree(b,x,z,s*1.25,int(x*17+z*13),'pine')
    b.collider('tree',(x,2*s,z),(.55*s,4*s,.55*s),'cylinder')


def boat(b,x,z,sail=True):
    o=Organic('boat')
    o.ball((x,.25,z),(.6,.28,1.4),'cream');o.ball((x,.43,z),(.47,.12,1.06),'wood')
    if sail:
        o.beam((x,.4,z),(x,3.6,z),.035,'wood')
        o.mesh([(x,3.6,z),(x,.6,z),(x+1.65,.6,z+.12)],[(0,1,2),(2,1,0)],'cream')
        o.mesh([(x,3.6,z),(x,.6,z),(x-.7,.6,z-.12)],[(0,1,2),(2,1,0)],'teal')
        o.beam((x,.6,z),(x+1.65,.6,z+.12),.025,'wood')
    else:
        o.ball((x,.5,z-.8),(.4,.22,.25),'teal');o.box((x,.6,z+.1),(.8,.4,.3),'glass')
    transfer(o,b)

def mediterranean(b):
    imported_rig(b)
    # Sea is clipped to the island's own perimeter, with a separate shallow shore.
    cfg=json.loads((ROOT/'src/features/journey/landscapes.json').read_text())['clubmed']
    outline=[]
    for i in range(129):
        a=i*math.tau/128;r=(abs(math.cos(a)/cfg['rx'])**cfg['power']+abs(math.sin(a)/cfg['rz'])**cfg['power'])**(-1/cfg['power'])*(1+cfg['scallop']*math.cos(3*a+cfg['phase']))
        outline.append((math.cos(a)*r,math.sin(a)*r))
    def clipped(edge):
        out=[]
        for a,c in zip(outline,outline[1:]):
            if a[0]<=edge:out.append(a)
            if (a[0]<=edge)!=(c[0]<=edge):
                t=(edge-a[0])/(c[0]-a[0]);out.append((edge,a[1]+t*(c[1]-a[1])))
        return out
    for edge,y,mat in [(-13.4,.07,'waterShallow'),(-14.7,.09,'waterDeep')]:
        points=clipped(edge);b.mesh([(x,y,z) for x,z in points],[tuple(reversed(range(len(points))))],mat)
    b.collider('sea',(-30,1,0),(32.8,3,60))
    def waves(part):
        for row in range(12):
            x=-14.3-row*.45
            for j in range(4):
                z=-7+j*4+math.sin(row)*.6
                if x*x/440+z*z/280<.86:
                    for k in range(7):part.beam((x+k*.08,.13,z+k*.3),(x+(k+1)*.08,.13,z+(k+1)*.3),.018,'foam',5)
    moving_part(b,'waves',(-14,0,0),waves)
    moving_part(b,'sailboat',(-16,0,-6),lambda p:boat(p,-16,-6))
    def waterski(part):
        boat(part,-15,5,False)
        part.beam((-15,.45,3.6),(-15,.8,1),.012,'cream',5)
        for x in [-15.18,-14.82]:part.box((x,.12,.7),(.12,.07,1.5),'red')
        # Small articulated silhouette, integrated at the tow point.
        o=Organic('skier')
        for dx in [-.13,.13]:o.curve([(-15+dx,.2,.7),(-15+dx,.65,.5),(-15+dx,1,.7)],.065,'skinDetail',10)
        o.ball((-15,1.2,.7),(.22,.3,.13),'red');o.ball((-15,1.65,.7),(.13,.17,.13),'skinDetail')
        for dx in [-.2,.2]:o.curve([(-15+dx,1.3,.7),(-15+dx,1.1,1),(-15+dx*.5,.8,1)],.045,'skinDetail',10)
        transfer(o,part)
    detail_palette();moving_part(b,'waterski',(-15,0,5),waterski)
    # Pine-lined beach, a pool and an open-air stage, outside the rig's cable envelope.
    for i,(x,z) in enumerate([(-10,-10),(-10,8),(9,-10.5),(18,-5)]):pine(b,x,z,.85+i*.05)
    b.box((13,.08,-8),(6,.22,4.8),'cream');b.box((13,.22,-8),(5.5,.08,4.3),'waterShallow')
    b.collider('pool',(13,.4,-8),(5.8,.8,4.6))
    for x in [10.2,15.8]:
        for z in [-9.5,-6.5]:b.ring((x,.4,z),.23,.025,'iron','z',16)
    b.collider('outdoor-stage',(13,.4,0),(6,.8,4))
    b.box((13,.4,0),(6,.8,4),'wood')
    for x in [10.2,15.8]:
        b.beam((x,0,-1.8),(x,4,-1.8),.1,'iron');b.box((x,2.8,-1.8),(.5,.9,.45),'iron')
    b.beam((10.2,4,-1.8),(15.8,4,-1.8),.09,'iron')
    for x in [11,12,13,14,15]:b.ball((x,3.9,-1.8),(.12,.15,.12),'lamp')
    sign(b,'THEATRE DE PLEIN AIR',13,3.25,-1.6,5.7)
    for row in range(3):
        z=3+row*.9;b.box((13,.5,z),(5,.12,.45),'oak');b.collider('theatre-bench',(13,.5,z),(5,1,.5))
        for x in [11,15]:b.beam((x,0,z),(x,.5,z),.055,'iron')
    for z in [-3,2,6]:
        x=-10.5;b.beam((x,0,z),(x,2.7,z),.045,'wood')
        for i in range(16):
            a=i*math.tau/16;c=(i+1)*math.tau/16
            b.mesh([(x,2.9,z),(x+math.cos(a)*1.3,2.3,z+math.sin(a)*1.3),(x+math.cos(c)*1.3,2.3,z+math.sin(c)*1.3)],[(0,1,2),(2,1,0)],'cream' if i%2 else 'teal')
        b.collider('parasol',(x,1.4,z),(.2,2.8,.2),'cylinder')
        b.box((x+1,.3,z+.2),(.7,.15,1.8),'wood');b.box((x+1,.5,z-.45),(.7,.65,.13),'cream',rot=(-.3,0,0));b.collider('lounger',(x+1,.5,z+.2),(.8,1,1.9))
    sign(b,'GREGOLIMANO · EUBEE',-10,2,-5.5,5.4,posts=True)
    sign(b,'BELDI · ANTALYA',12,2,7,4.8,posts=True)

def caravan(b,x,z,color='teal',truck=False):
    o=Organic('announcement-truck' if truck else 'caravan')
    o.box((x,1.25,z),(2.6,1.8,4.5),'cream');o.box((x,.8,z),(2.65,.65,4.55),color)
    o.ball((x,2.15,z),(1.35,.32,2.3),'cream')
    for side in [-1,1]:
        for dz in [-1.35,1.35]:
            o.ball((x+side*1.28,.48,z+dz),(.19,.46,.46),'iron');o.ring((x+side*1.48,.48,z+dz),.27,.04,'brass','x')
        for dz in [-1.2,.3]:
            o.box((x+side*1.34,1.6,z+dz),(.06,.65,.85),'wood');o.box((x+side*1.38,1.6,z+dz),(.03,.52,.7),'glass')
        o.beam((x+side*1.37,1.32,z-1.2),(x+side*1.37,1.88,z-1.2),.018,'brass')
    o.box((x,1.4,z+2.29),(.8,1.45,.09),color);o.ball((x+.27,1.4,z+2.36),(.045,.045,.045),'brass')
    for i in range(3):o.box((x,.15+i*.16,z+2.9-i*.2),(1,.14,.4),'wood')
    if truck:
        o.box((x,1.6,z-2.3),(2.2,.7,.04),'glass')
        for side in [-1,1]:
            o.ball((x+side*.6,2.65,z),(.35,.25,.35),'iron');o.ring((x+side*.6,2.65,z+.31),.23,.04,'brass','z')
    transfer(o,b);b.collider('announcement-truck' if truck else 'caravan',(x,1.3,z),(2.9,2.6,5.8))

def elephant(b,x,z):
    material('elephant','#8f9391',rough=.93);material('elephantEar','#969993',rough=.95)
    o=Organic('elephant');p=lambda a:(x+a[0],a[1],z+a[2])
    o.ball(p((0,2.1,0)),(1.45,1.1,.85),'elephant',segments=40,rings=28)
    o.ball(p((1.2,2.55,0)),(.64,.76,.65),'elephant',segments=32,rings=24)
    for dx in [-.85,.8]:
        for dz in [-.51,.51]:
            o.profile([(y,x+dx+cx,z+dz,rx,rz) for y,cx,rx,rz in [(.06,0,.3,.29),(.22,0,.31,.3),(.75,.04,.24,.24),(1.3,-.04,.3,.29),(2,0,.4,.36)]],'elephant',24)
            for j in [-1,0,1]:o.ball(p((dx+.22,.13,dz+j*.15)),(.1,.1,.075),'stoneLight',segments=12,rings=8)
    for side in [-1,1]:
        o.ball(p((.85,2.55,side*.72)),(.64,.81,.12),'elephant',rot=(0,side*.2,side*.1),segments=28,rings=20)
        o.ball(p((.93,2.56,side*.815)),(.49,.62,.045),'elephantEar',segments=24,rings=16)
        o.ball(p((1.55,2.75,side*.44)),(.084,.065,.045),'elephantEar')
        o.ball(p((1.57,2.75,side*.47)),(.053,.035,.02),'eye')
        o.ball(p((1.58,2.765,side*.486)),(.013,.012,.008),'sclera',segments=12,rings=8)
        o.curve([p((1.48,2.78,side*.45)),p((1.55,2.815,side*.477)),p((1.64,2.78,side*.45))],.024,'elephant',10)
        o.curve([p((1.62,2.1,side*.34)),p((2.05,1.95,side*.36)),p((2.3,2.18,side*.37))],.085,'cream',14,taper=.5)
        for i in range(5):o.curve([p((.65+i*.08,2.2,side*.824)),p((.57+i*.07,2.55,side*.836)),p((.6+i*.05,2.95,side*.8))],.009,'elephant',6)
        for i in range(6):
            # Fine shoulder folds follow the curved flank, avoiding a projected checker texture.
            xx=.24+i*.07
            o.curve([p((xx,2.65,side*.73)),p((xx-.06,2.25,side*.85)),p((xx-.13,1.8,side*.8))],.008,'elephantEar',6)
    o.curve([p((-1.3,2.3,0)),p((-1.62,1.8,0)),p((-1.6,1.3,.2))],.055,'elephant',10,taper=.3)
    o.ball(p((-1.6,1.25,.2)),(.08,.16,.08),'hairDetail')
    transfer(o,b)
    def trunk(part):
        o=Organic('elephant-trunk')
        o.curve([p((1.65,2.55,0)),p((1.98,2.1,0)),p((2.08,1.4,0)),p((2.18,.85,0)),p((2.5,.88,0)),p((2.6,1.2,0))],.19,'elephant',20,taper=.18)
        for i in range(9):o.curve([p((2.05,1.4+i*.09,-.13)),p((2.17,1.4+i*.09,0)),p((2.05,1.4+i*.09,.13))],.013,'elephantEar',6)
        transfer(o,part)
    moving_part(b,'elephant-trunk',p((1.65,2.55,0)),trunk)
    b.collider('elephant',(x+.3,1.7,z),(4.5,3.4,1.9))

def lion(b,x,z):
    material('lion','#c49355',rough=.88);material('mane','#735037',rough=.97);material('maneLight','#98704b',rough=.94)
    material('lionMuzzle','#dac5a0',rough=.9);material('lionAmber','#b99b49',rough=.4)
    o=Organic('lion');p=lambda a:(x+a[0],a[1],z+a[2])
    o.ball(p((0,.9,0)),(1,.46,.39),'lion',segments=32,rings=20)
    for dx in [-.65,.57]:
        for dz in [-.25,.25]:
            o.curve([p((dx,1,dz)),p((dx-.1,.5,dz)),p((dx+.08,.15,dz))],.12,'lion',14)
            o.ball(p((dx+.18,.11,dz)),(.21,.13,.14),'lion')
            for k in [-1,0,1]:o.curve([p((dx+.28,.14,dz+k*.075)),p((dx+.36,.07,dz+k*.075))],.009,'mane',6)
    o.ball(p((.8,1.25,0)),(.45,.53,.45),'mane',segments=32,rings=24)
    for i in range(190):
        a=i*2.399963;u=-1+2*(i+.5)/190;r=math.sqrt(1-u*u)
        start=(.8+.44*u,1.25+.535*r*math.cos(a),.46*r*math.sin(a))
        end=(start[0]-.12,start[1]-.13,start[2]*1.04)
        middle=((start[0]+end[0])/2+.035,(start[1]+end[1])/2+.045,(start[2]+end[2])/2+math.sin(a)*.025)
        o.curve([p(start),p(middle),p(end)],.035,'maneLight' if i%5==0 else 'mane',9,taper=.4)
    o.ball(p((1.02,1.3,0)),(.34,.32,.29),'lion')
    for side in [-1,1]:
        o.ball(p((1.27,1.2,side*.095)),(.16,.11,.12),'lionMuzzle');o.ball(p((1.22,1.43,side*.2)),(.052,.039,.03),'eye')
        o.ball(p((1.24,1.43,side*.22)),(.033,.026,.012),'lionAmber')
        o.ball(p((1.253,1.43,side*.23)),(.011,.021,.007),'eye')
        o.ball(p((1.26,1.442,side*.232)),(.007,.006,.003),'sclera',segments=10,rings=6)
        o.curve([p((1.15,1.47,side*.22)),p((1.22,1.484,side*.23)),p((1.28,1.46,side*.20))],.019,'lion',8)
        o.ball(p((.9,1.64,side*.26)),(.11,.12,.055),'lion')
        for j in range(3):o.curve([p((1.32,1.23-j*.025,side*.12)),p((1.39,1.26-j*.02,side*.38))],.004,'cream',5)
    o.ball(p((1.39,1.25,0)),(.06,.05,.08),'eye')
    for side in [-1,1]:o.curve([p((1.42,1.18,0)),p((1.36,1.135,side*.08)),p((1.25,1.14,side*.15))],.009,'mane',6)
    o.curve([p((-1,.95,0)),p((-1.4,1.1,.15)),p((-1.6,.75,.35))],.035,'lion',10);o.ball(p((-1.6,.74,.35)),(.07,.1,.07),'mane')
    transfer(o,b);b.collider('lion',(x+.05,.85,z),(3.4,1.7,1.2))

def circus_backstage(b):
    detail_palette()
    caravan(b,-9,-7,'teal');caravan(b,9,-8,'red');caravan(b,-11,5,'red',True)
    sign(b,'BOUGLIONE · EN TOURNEE',-11,2.2,7.4,4.7)
    # An architectural vignette recalls the Paris venue without pretending to reproduce its plan.
    b.box((0,2.2,-11.1),(10,4.4,1.6),'brick')
    for x in [-4,-2,0,2,4]:
        b.box((x,2,-10.2),(.2,4,.2),'stoneLight')
        b.box((x+.65,1.35,-10.18),(1,2.4,.12),'darkwood')
        for k in range(11):
            a=k*math.pi/10;b.ball((x+.65+.5*math.cos(a),2.45+.5*math.sin(a),-10.05),(.09,.12,.1),'stoneLight')
    sign(b,'CIRQUE D’HIVER · PARIS',0,3.6,-10.1,9)
    b.collider('winter-circus-facade',(0,2.3,-11.1),(10,4.6,1.8))
    elephant(b,-9,0);lion(b,-1,9)
    # Animal areas and working props are separated from the audience routes.
    for cx,cz,w,d in [(-9,0,6,4.4),(-1,9,4.7,3.5)]:
        for side in [-1,1]:
            z=cz+side*d/2
            for x in [cx-w/2,cx,cx+w/2]:b.beam((x,0,z),(x,.9,z),.045,'wood')
            b.beam((cx-w/2,.65,z),(cx+w/2,.65,z),.018,'cream')
            b.collider('animal-area',(cx,.4,z),(w,.8,.12))
    for x,z in [(-5.8,-7),(-5.8,-8.4),(6.8,-4.5)]:crate(b,x,0,z,.85)
    for i in range(6):b.beam((5.8,.15+i*.12,-6),(7.8,.15+i*.12,-6),.05,'iron')
    b.collider('rigging-stock',(6.8,.45,-6),(2.1,.9,.5))
    for i in range(4):b.ring((5.8,.1+i*.055,-4.7),.4,.026,'cream')
    b.box((-6,.9,3.4),(1.4,1.8,.6),'iron');b.box((-6,1.83,3.4),(1.5,.1,.7),'wood')
    for i in range(8):b.ball((-6.5+i*.14,1.9,3.4),(.035,.04,.035),'lamp' if i%2 else 'red')
    b.collider('show-control',(-6,.95,3.4),(1.5,1.9,.7))
    for x in [-5.5,-4.3]:
        b.beam((x,0,7.6),(x,2.4,7.6),.05,'wood')
    b.box((-4.9,1.5,7.6),(1.4,1.9,.12),'cream')
    sign(b,'CE SOIR',-4.9,2,7.7,1.4,'red')
    sign(b,'BOUGLIONE',-4.9,1.4,7.7,2,'red')
    sign(b,'LA PISTE & LES COULISSES',0,3,2.4,6.3,posts=True)
