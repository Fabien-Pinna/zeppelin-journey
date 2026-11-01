"""Detailed original cast, keeping the existing gameplay hand/foot contract."""
import math, random
import bpy
from mathutils import Vector
from craft import OUT, export
from organic import Organic, detail_palette, catmull


def character(asset='traveller',backpack=True):
    detail_palette()
    objects=[]
    root=bpy.data.objects.new('Traveller',None);bpy.context.scene.collection.objects.link(root);objects.append(root)
    def part(name,pivot,draw):
        joint=bpy.data.objects.new(name,None);bpy.context.scene.collection.objects.link(joint)
        joint.parent=root;joint.location=(pivot[0],-pivot[2],pivot[1]);objects.append(joint)
        b=Organic(asset+'-'+name);draw(b)
        meshes=b.finish(parent=joint)
        for obj in meshes:
            for v in obj.data.vertices:v.co-=joint.location
        objects.extend(meshes)

    def body(b):
        b.profile([(.85,0,0,.17,.12),(.91,0,0,.225,.14),(1.0,0,0,.225,.14)],'trousers')
        # Sculpted waist/chest/shoulders instead of an ellipsoid torso.
        b.profile([(0.94,0,0,.235,.145),(1.03,0,0,.24,.155),(1.2,0,-.012,.255,.175),(1.43,0,-.015,.29,.18),(1.52,0,-.025,.26,.15),(1.59,0,-.01,.12,.10)],'coatDetail')
        b.profile([(1.43,0,.13,.14,.045),(1.58,0,.07,.105,.055),(1.62,0,.02,.075,.055)],'shirt',24)
        b.profile([(1.56,0,0,.085,.08),(1.73,0,.01,.09,.085)],'skinDetail',24)
        for s in [-1,1]:
            b.curve([(s*.10,1.58,.12),(s*.20,1.49,.17),(s*.11,1.32,.183)],.028,'coatDetail',10)
            b.curve([(s*.22,1.36,.115),(s*.205,1.2,.146),(s*.18,1.04,.148)],.006,'stitch',6)
            b.box((s*.16,1.19,.161),(.155,.18,.045),'coatDetail')
            b.curve([(s*.235,1.275,.19),(s*.16,1.25,.203),(s*.085,1.275,.19)],.013,'leatherDetail')
            b.ball((s*.16,1.255,.205),(.014,.014,.008),'brass',segments=12,rings=8)
        b.curve([(0,1.04,.163),(0,1.25,.181),(0,1.46,.174)],.012,'leatherEdge')
        for y in [1.07,1.19,1.31,1.43]:b.ball((0,y,.192),(.016,.016,.009),'brass',segments=12,rings=8)
        b.profile([(.96,0,0,.243,.151),(1.015,0,0,.247,.157)],'leatherDetail',32,1)
        b.box((0,.988,.168),(.085,.064,.025),'brass');b.box((0,.988,.184),(.052,.036,.009),'leatherDetail')
        # Scarf wraps, soft draped tails, stitched hems.
        for i in range(3):
            b.curve([(-.10,1.60+i*.016,-.045),(-.13,1.61+i*.012,.05),(0,1.585+i*.017,.14),(.13,1.61+i*.012,.05),(.1,1.60+i*.016,-.045)],.026,'scarf',10)
        b.curve([(.07,1.59,.15),(.11,1.48,.205),(.10,1.33,.23),(.16,1.2,.25)],.048,'scarf',10,taper=.1)
        b.curve([(.105,1.53,.237),(.125,1.42,.26),(.14,1.29,.27)],.004,'stitch',5)
        if backpack:
            b.profile([(1.02,0,-.275,.16,.09),(1.1,0,-.29,.225,.12),(1.41,0,-.28,.235,.13),(1.53,0,-.265,.19,.10),(1.56,0,-.25,.15,.08)],'leatherDetail')
            # Rounded flap, gusset seams, two buckled straps and front pocket.
            b.ball((0,1.46,-.395),(.223,.12,.044),'leatherDetail')
            for s in [-1,1]:
                b.curve([(s*.17,1.52,-.33),(s*.23,1.52,-.12),(s*.23,1.47,.11),(s*.21,1.11,.15),(s*.17,1.04,-.27)],.029,'leatherDetail',10)
                b.curve([(s*.215,1.45,-.35),(s*.225,1.19,-.37),(s*.17,1.07,-.36)],.006,'stitch',5)
                b.box((s*.115,1.33,-.418),(.045,.29,.018),'leatherEdge')
                b.box((s*.115,1.28,-.438),(.071,.075,.015),'brass')
                b.box((s*.115,1.28,-.449),(.045,.047,.009),'leatherDetail')
                for y in [1.15,1.19,1.23]:b.ball((s*.115,y,-.432),(.004,.005,.003),'darkwood',segments=8,rings=6)
            b.box((0,1.16,-.423),(.14,.15,.055),'leatherDetail')
            b.curve([(-.08,1.55,-.28),(-.065,1.63,-.29),(.065,1.63,-.29),(.08,1.55,-.28)],.018,'leatherDetail')
            b.ball((0,1.57,-.26),(.29,.074,.078),'shirt')
            for x in [-.18,.18]:b.ring((x,1.57,-.26),.077,.012,'leatherDetail','x',24)
    part('Body',(0,1.1,0),body)

    def head(b):
        b.profile([(1.70,0,.055,.065,.075),(1.74,0,.045,.125,.115),(1.80,0,.018,.165,.155),(1.89,0,0,.198,.176),(1.98,0,-.015,.196,.179),(2.08,0,-.024,.184,.17),(2.15,0,-.03,.14,.13),(2.19,0,-.03,.035,.035)],'skinDetail',48,4)
        for s in [-1,1]:
            b.ball((s*.195,1.91,-.007),(.041,.075,.043),'skinDetail')
            b.ball((s*.218,1.918,.019),(.018,.041,.02),'skinRose',segments=16,rings=10)
            b.curve([(s*.217,1.88,.035),(s*.228,1.92,.039),(s*.212,1.952,.036)],.008,'skinDetail')
            # Cheek planes and eye sockets inset into the face, with actual lids.
            b.ball((s*.081,1.965,.151),(.039,.020,.016),'sclera')
            b.ball((s*.078,1.965,.166),(.017,.018,.005),'iris',segments=20,rings=12)
            b.ball((s*.078,1.965,.171),(.008,.011,.003),'eye',segments=16,rings=10)
            b.ball((s*.073,1.972,.175),(.003,.003,.002),'sclera',segments=8,rings=6)
            b.curve([(s*.04,1.963,.157),(s*.079,1.985,.166),(s*.12,1.967,.139)],.008,'skinDetail',8)
            b.curve([(s*.04,1.962,.159),(s*.08,1.948,.17),(s*.12,1.965,.141)],.005,'skinDetail',8)
            b.curve([(s*.037,2.008,.166),(s*.077,2.025,.172),(s*.131,2.016,.143)],.013,'hairDetail',8,taper=.35)
        b.profile([(1.867,0,.184,.031,.026),(1.89,0,.192,.037,.037),(1.94,0,.173,.025,.034),(1.995,0,.153,.016,.014)],'skinDetail',24)
        for s in [-1,1]:
            b.ball((s*.029,1.879,.193),(.019,.017,.021),'skinDetail',segments=16,rings=10)
            b.ball((s*.023,1.869,.206),(.009,.004,.008),'lip',segments=12,rings=8)
        b.curve([(-.061,1.814,.164),(-.027,1.806,.18),(0,1.809,.185),(.028,1.807,.179),(.059,1.82,.165)],.006,'lip',8)
        b.curve([(-.045,1.8,.173),(0,1.789,.178),(.045,1.803,.172)],.008,'skinRose',8,taper=.4)
        # A swept hairstyle, asymmetrical locks and fine strand ridges.
        verts=[];faces=[];segments=48;rings=14
        def scalp(a,t,extra=0):
            end=1.38-.24*math.sin(a)+.055*math.sin(a*5+.4)
            phi=t*end
            return ((.204+extra)*math.sin(phi)*math.cos(a),2.015+(.212+extra)*math.cos(phi),-.04+(.181+extra)*math.sin(phi)*math.sin(a))
        for j in range(rings+1):
            for i in range(segments):verts.append(scalp(math.tau*i/segments,j/rings))
        for j in range(rings):
            for i in range(segments):faces.append((j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i))
        b.mesh(verts,faces,'hairDetail',True)
        def lock(points,width,depth,mat='hairDetail'):
            points=catmull(points,5);verts=[];sides=12
            for j,p in enumerate(points):
                t=j/(len(points)-1)
                tangent=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized()
                normal=(p-Vector((0,2.015,-.04))).normalized()
                side=tangent.cross(normal).normalized()
                up=side.cross(tangent).normalized()
                taper=max(.025,math.sin(math.pi*t))**.55
                for k in range(sides):
                    a=k*math.tau/sides
                    verts.append(p+(side*math.cos(a)*width+up*math.sin(a)*depth)*taper)
            faces=[(j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k) for j in range(len(points)-1) for k in range(sides)]
            b.mesh(verts,faces,mat,True)
        rng=random.Random(72)
        # Overlapping broad tapered locks, with uneven swept tips rather than a comb-shaped cap.
        for i in range(23):
            a=i*math.tau/23+rng.uniform(-.08,.08)
            tip=rng.uniform(.96,1.12)
            points=[scalp(a+.8*(1-t),t,.012+.014*math.sin(math.pi*t)) for t in [.12,.35,.6,.85,tip]]
            lock(points,rng.uniform(.027,.043),.015)
        for i in range(10):
            t=i/9
            points=[(-.16+t*.17,2.13,-.095),(-.13+t*.19,2.215+.012*math.sin(i*.7),-.025),(-.04+t*.20,2.24+.008*math.sin(i),.065),(.055+t*.14,2.105+.05*t,.15)]
            lock(points,.037,.010,'hairDetail')
    part('Head',(0,1.63,0),head)

    for s,label in [(-1,'Left'),(1,'Right')]:
        def arm(b,s=s):
            b.profile([(.92,s*.4,.015,.073,.075),(1.04,s*.40,.009,.082,.09),(1.16,s*.38,-.01,.089,.095),(1.32,s*.35,-.008,.103,.103),(1.46,s*.32,0,.108,.11),(1.53,s*.29,0,.105,.10),(1.57,s*.28,0,.08,.065),(1.59,s*.27,0,.01,.01)],'shirt')
            for i in range(3):
                y=1.02+i*.034
                b.curve([(s*.32,y,.03),(s*.4,y-.012,.098),(s*.475,y+.01,.024)],.009,'shirt',8)
            b.profile([(.92,s*.4,.015,.078,.081),(.97,s*.4,.015,.081,.085),(1.0,s*.4,.015,.077,.082)],'shirt',24,2)
            b.curve([(s*.35,.946,.087),(s*.4,.94,.1),(s*.45,.946,.087)],.004,'stitch',6)
            b.ball((s*.4,.85,.018),(.064,.086,.044),'skinDetail')
            # Four individual curled fingers and thumb, staying at the trapeze grip.
            for i in range(4):
                x=s*(.354+i*.028)
                b.curve([(x,.842,.034),(x,.785-.006*(i%2),.046),(x,.782,.073),(x,.817,.075)],.014,'skinDetail',8)
                b.ball((x,.812,.085),(.010,.014,.0025),'skinRose',segments=8,rings=6)
            b.curve([(s*.346,.883,.025),(s*.324,.843,.07),(s*.349,.824,.083)],.022,'skinDetail',10)
        part(label+'Arm',(s*.31,1.52,0),arm)
        def leg(b,s=s):
            x=s*.145
            b.profile([(.25,x,0,.083,.09),(.36,x,-.008,.097,.11),(.50,x,.008,.103,.125),(.62,x,.018,.108,.117),(.78,x,0,.123,.134),(.98,x,-.01,.125,.139)],'trousers')
            b.curve([(x+s*.10,.35,.018),(x+s*.112,.57,.026),(x+s*.12,.87,.02)],.004,'stitch',6)
            for i in range(3):b.curve([(x-.07,.36+i*.035,.07),(x,.345+i*.035,.108),(x+.073,.36+i*.035,.074)],.008,'trousers',8)
            b.profile([(.09,x,.04,.12,.185),(.16,x,.045,.126,.20),(.22,x,.015,.105,.15),(.32,x,-.015,.09,.105)],'leatherDetail')
            b.profile([(.025,x,.06,.123,.193),(.07,x,.06,.13,.202),(.09,x,.06,.125,.19)],'darkwood',32,2)
            b.curve([(x-.1,.13,.11),(x-.072,.16,.21),(x+.072,.16,.21),(x+.1,.13,.11)],.005,'stitch',6)
            for i in range(4):
                y=.20+i*.025;z=.155-i*.028
                for side in [-1,1]:b.ball((x+side*.05,y,z),(.011,.01,.007),'brass',segments=8,rings=6)
                b.curve([(x-.05,y,z),(x+.05,y+.02,z-.021)],.004,'stitch',6)
                b.curve([(x+.05,y,z),(x-.05,y+.02,z-.021)],.004,'stitch',6)
        part(label+'Leg',(s*.155,.94,0),leg)
    export(objects,OUT/(asset+'.glb'))
    for obj in objects:obj.hide_set(True);obj.hide_render=True
    return objects
