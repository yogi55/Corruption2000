import numpy as np, random, math, json
from PIL import Image

BW=154            # base diamond width in pixels (pixel-art grid)
BH=BW//2          # diamond height
SL=4              # slab thickness (base px)
SC=3              # upscale factor -> 462 px wide cells
OUT='/home/claude/corruption2000/assets/sp/'

ASPH=(74,79,87); ASPH_D=(54,58,65); SIDE=(160,162,167); SIDE_J=(143,145,151); CURB=(206,207,211)
OUTL=(28,30,34); LINE=(226,223,206); ZEBRA=(232,232,226)
SW=.17

def uv(x,y):
    a=(x+.5-BW/2)/(BW/2); b=(y+.5)/(BH/2)
    return (a+b)/2,(b-a)/2

def inside(x,y):
    u,v=uv(x,y); return -1e-9<=u<=1+1e-9 and -1e-9<=v<=1+1e-9

def shade(c,f): return tuple(max(0,min(255,int(ch*f))) for ch in c)

def proj(u,v,z=0):
    return int(BW/2+(u-v)*BW/2), int((u+v)*BH/2*1.0 - z)  # y in [0,BW/2]... (u+v)*BH/2*? see below

def pj(u,v,z=0):
    # pixel position of tile point (u,v) at height z (base px)
    return BW/2+(u-v)*BW/2, (u+v)*BH/2-z

def road_class(u,v,m,rr=.075,RR=.12):
    A,B,C,D=bool(m&1),bool(m&2),bool(m&4),bool(m&8)
    ok_u=SW<=u<=1-SW; ok_v=SW<=v<=1-SW
    asph=False
    if ok_u and ok_v: asph=True
    if A and u<SW and ok_v: asph=True
    if B and u>1-SW and ok_v: asph=True
    if C and v<SW and ok_u: asph=True
    if D and v>1-SW and ok_u: asph=True
    # inner fillets (sidewalk island corners rounded) where both arms present
    for (cu,cv,a1,a2,su,sv) in ((0,0,A,C,1,1),(1,0,B,C,-1,1),(0,1,A,D,1,-1),(1,1,B,D,-1,-1)):
        if a1 and a2:
            ex=SW if cu==0 else 1-SW; ey=SW if cv==0 else 1-SW
            # island square: u beyond ex outward, v beyond ey outward
            ou=(u<ex) if cu==0 else (u>ex); ov=(v<ey) if cv==0 else (v>ey)
            if ou and ov:
                du=abs(u-ex); dv=abs(v-ey)
                if du<rr and dv<rr:
                    # circle centre at (ex +- rr toward outside)
                    cx_=rr-du; cy_=rr-dv
                    if cx_*cx_+cy_*cy_<rr*rr: pass
                    else: asph=True
                    # inside circle region stays sidewalk
        elif (not a1) and (not a2):
            # outer rounding of asphalt corner
            ex=SW if cu==0 else 1-SW; ey=SW if cv==0 else 1-SW
            inu=(u>=ex) if cu==0 else (u<=ex); inv=(v>=ey) if cv==0 else (v<=ey)
            if inu and inv and ok_u and ok_v:
                du=abs(u-ex); dv=abs(v-ey)
                if du<RR and dv<RR:
                    if (RR-du)**2+(RR-dv)**2>RR*RR: asph=False
    return asph

def render_cell(m,state,seed,kind='road'):
    rng=random.Random(seed)
    H=BH+SL
    top=np.zeros((H,BW),bool); cls=np.zeros((H,BW),np.int8)  # 0 outside,1 sidewalk,2 asphalt
    UV=np.zeros((H,BW,2))
    for y in range(BH):
        for x in range(BW):
            if inside(x,y):
                u,v=uv(x,y); UV[y,x]=(u,v); top[y,x]=True
                cls[y,x]=2 if road_class(u,v,m) else 1
    img=np.zeros((H,BW,4),np.uint8)
    # base colours
    for y in range(BH):
        for x in range(BW):
            if not top[y,x]: continue
            u,v=UV[y,x]
            if cls[y,x]==2:
                n=((x*7+y*13)%5==0)*3+((x//2*5+y//2*11)%7==0)*2
                c=tuple(ch+n-2 for ch in ASPH)
            else:
                ju=(u*9)%1<.11; jv=(v*9)%1<.11
                c=SIDE_J if (ju or jv) else SIDE
            img[y,x]=(*c,255)
    # curb / edge shading
    base=img.copy()
    for y in range(BH):
        for x in range(BW):
            if not top[y,x]: continue
            nb=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            ncls=[cls[yy,xx] if 0<=yy<H and 0<=xx<BW else 0 for xx,yy in nb]
            if cls[y,x]==1 and 2 in ncls: base[y,x]=(*CURB,255)
            elif cls[y,x]==2 and 1 in ncls: base[y,x]=(*ASPH_D,255)
    img=base
    A,B,C,D=bool(m&1),bool(m&2),bool(m&4),bool(m&8)
    narms=sum((A,B,C,D))
    def setp(x,y,c):
        if 0<=x<BW and 0<=y<BH and top[y,x] and cls[y,x]==2: img[y,x]=(*c,255)
    # markings
    for y in range(BH):
        for x in range(BW):
            if not (top[y,x] and cls[y,x]==2): continue
            u,v=UV[y,x]
            inU=(u<SW or u>1-SW); inV=(v<SW or v>1-SW)
            # centre line along u (for arms A/B)
            if abs(v-.5)<.014 and (A or B):
                allow=(narms<=2 and (A and B)) or (narms>=3 and inU) or (narms==2 and (A or B) and inU)
                if allow and ((u*8)%1)<.55 and ((A and u<.5) or (B and u>.5) or (A and B)): img[y,x]=(*LINE,255)
            if abs(u-.5)<.014 and (C or D):
                allow=(narms<=2 and (C and D)) or (narms>=3 and inV) or (narms==2 and (C or D) and inV)
                if allow and ((v*8)%1)<.55 and ((C and v<.5) or (D and v>.5) or (C and D)): img[y,x]=(*LINE,255)
            # zebra on arms for junctions
            if narms>=3:
                if A and .02<u<.14 and SW<v<1-SW and int(v*15)%2==0: img[y,x]=(*ZEBRA,255)
                if B and .86<u<.98 and SW<v<1-SW and int(v*15)%2==0: img[y,x]=(*ZEBRA,255)
                if C and .02<v<.14 and SW<u<1-SW and int(u*15)%2==0: img[y,x]=(*ZEBRA,255)
                if D and .86<v<.98 and SW<u<1-SW and int(u*15)%2==0: img[y,x]=(*ZEBRA,255)
    # wear
    asph_px=[(x,y) for y in range(BH) for x in range(BW) if top[y,x] and cls[y,x]==2 and 3<x<BW-4 and 3<y<BH-2]
    if kind=='road' and asph_px:
        if state in (1,2):
            for _ in range(3 if state==1 else 5):
                x,y=rng.choice(asph_px); d=rng.choice([(1,0),(0,1),(1,1),(1,-1)])
                for i in range(rng.randint(6,16)):
                    setp(x,y,(44,47,53));
                    if rng.random()<.5: setp(x+1,y,(44,47,53))
                    x+=d[0]; y+=d[1]
                    if rng.random()<.35: d=rng.choice([(1,0),(0,1),(1,1),(1,-1),(-1,1)])
        if state==2:
            for _ in range(rng.randint(3,5)):
                x,y=rng.choice(asph_px); r=rng.choice([1.3,1.8,2.4])
                for yy in range(int(y-3),int(y+4)):
                    for xx in range(int(x-4),int(x+5)):
                        dx=(xx-x)/1.5; dy=(yy-y)
                        d=math.hypot(dx,dy)
                        if d<r+rng.random()*.5: setp(xx,yy,(30,32,37))
                        elif d<r+1.3 and rng.random()<.6: setp(xx,yy,(88,92,100))
        if state==3:
            for _ in range(2):
                x,y=rng.choice(asph_px); w=rng.randint(5,9); h=rng.randint(3,5)
                for yy in range(y-h,y+h+1):
                    for xx in range(x-w,x+w+1):
                        e=(abs(xx-x)==w or abs(yy-y)==h)
                        setp(xx,yy,(88,92,99) if e else (58,61,67))
    # slab (front edges only where no arm)
    for y in range(BH,H):
        for x in range(BW):
            for s in range(1,SL+1):
                yy=y-s
                if 0<=yy<BH and top[yy,x]:
                    u,v=UV[yy,x]
                    left=x<BW/2
                    if left and D: break
                    if (not left) and B: break
                    col=shade(SIDE_J,.8 if left else .62)
                    img[y,x]=(*col,255); cls[y,x]=3; break
    # also slab pixels filling gap beside bottom vertex handled above
    sil=(img[...,3]>0)
    # outline on silhouette boundary except where arm continues
    out=img.copy()
    for y in range(H):
        for x in range(BW):
            if not sil[y,x]: continue
            miss=None
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                xx,yy=x+dx,y+dy
                if not(0<=xx<BW and 0<=yy<H) or not sil[yy,xx]:
                    miss=(dx,dy); break
            if miss is None: continue
            # which edge? use own uv or nearby
            if top[y,x]:
                u,v=UV[y,x]
                edge=None
                best=min((u,'A'),(1-u,'B'),(v,'C'),(1-v,'D'))
                edge=best[1]
                if edge=='A' and A: continue
                if edge=='B' and B: continue
                if edge=='C' and C: continue
                if edge=='D' and D: continue
            out[y,x]=(*OUTL,255)
    return np.kron(out,np.ones((SC,SC,1),np.uint8)).astype(np.uint8)

def bridge_cell(axis,state,seed):
    # axis 'x': arms A,B; 'y': arms C,D. extra top margin for rails and deep girders below
    rng=random.Random(seed)
    m=3 if axis=='x' else 12
    M=8; GD=10
    H=M+BH+GD
    cell=np.zeros((H,BW,4),np.uint8)
    base=render_cell(m,state,seed)  # scaled; we need base res -> downscale by sampling
    b=base[::SC,::SC]  # BH+SL rows
    # replace slab by girders: copy top face part only (first BH rows)
    top=b[:BH].copy()
    # deck sidewalk strips narrower & rails
    cell[M:M+BH]=top
    # girders: for pixels under front edges
    sil=(top[...,3]>0)
    for y in range(BH,BH+GD):
        for x in range(BW):
            for s in range(1,GD+1):
                yy=y-s
                if 0<=yy<BH and sil[yy,x]:
                    left=x<BW/2
                    # girder only under front edges (D for left, B for right)
                    col=(112,114,122) if left else (84,86,94)
                    if s<=SL: col=shade(SIDE_J,.8 if left else .62)
                    if s>SL and (x%7==0): col=shade(col,.78)
                    cell[M+y,x]=(*col,255); break
    # outlines for girders bottom
    sil2=(cell[...,3]>0)
    for y in range(H):
        for x in range(BW):
            if sil2[y,x]:
                for dx,dy in ((0,1),):
                    yy=y+dy
                    if yy>=H or not sil2[yy,x]:
                        if y>=M+BH: cell[y,x]=(*OUTL,255)
    # rails along both side edges
    def rail(v_edge=None,u_edge=None):
        pts=[]
        steps=160
        for i in range(steps+1):
            t=i/steps
            u,v=(t,v_edge) if v_edge is not None else (u_edge,t)
            px,py=pj(u,v)
            pts.append((t,px,py))
        # posts every 1/8
        for k in range(9):
            t=k/8
            u,v=(t,v_edge) if v_edge is not None else (u_edge,t)
            px,py=pj(u,v); x=int(px); y=int(py)
            for z in range(0,6):
                yy=M+y-z-1
                if 0<=x<BW and 0<=yy<H: cell[yy,x]=(*(205,206,212),255)
            if 0<=x<BW and 0<=M+y-6<H: cell[M+y-6,x]=(*OUTL,255)
        for t,px,py in pts:
            x=int(px); y=int(py)
            yy=M+y-5
            if 0<=x<BW and 0<=yy<H: cell[yy,x]=(*(190,192,198),255)
            yy=M+y-6
            if 0<=x<BW and 0<=yy<H: cell[yy,x]=(*OUTL,255)
    if axis=='x':
        rail(v_edge=.0); rail(v_edge=1.0)
    else:
        rail(u_edge=.0); rail(u_edge=1.0)
    return np.kron(cell,np.ones((SC,SC,1),np.uint8)).astype(np.uint8), M

def parking_cell(orient,state,seed):
    rng=random.Random(seed)
    H=BH+SL
    top=np.zeros((H,BW),bool); UV=np.zeros((H,BW,2))
    img=np.zeros((H,BW,4),np.uint8)
    PAV=(92,97,104)
    for y in range(BH):
        for x in range(BW):
            if inside(x,y):
                u,v=uv(x,y); UV[y,x]=(u,v); top[y,x]=True
                n=((x*7+y*13)%5==0)*3+((x//2*5+y//2*11)%7==0)*2
                c=tuple(ch+n-2 for ch in PAV)
                uu,vv=(u,v) if orient==0 else (v,u)
                # bay lines: lines at uu = .05+k*.225 for k=0..4 over vv in [.05,.40] & [.60,.95]
                for k in range(5):
                    lu=.05+k*.225
                    if abs(uu-lu)<.011 and ((.05<vv<.40) or (.60<vv<.95)): c=(230,230,226)
                if (abs(vv-.40)<.011 or abs(vv-.60)<.011) and .05<uu<.95: c=(214,214,208)
                # arrows in aisle
                if abs(vv-.5)<.012 and ((uu*6)%1)<.4 and .08<uu<.92: c=(200,200,196)
                img[y,x]=(*c,255)
    if state==1:
        for _ in range(3):
            x=rng.randint(30,BW-30); y=rng.randint(10,BH-8)
            for yy in range(y-3,y+4):
                for xx in range(x-6,x+7):
                    if 0<=xx<BW and 0<=yy<BH and top[yy,xx] and ((xx-x)/2)**2+(yy-y)**2<5+rng.random():
                        img[yy,xx]=(66,70,77,255)
        for _ in range(4):
            x=rng.randint(25,BW-25); y=rng.randint(10,BH-8)
            for i in range(rng.randint(5,12)):
                if 0<=x<BW and 0<=y<BH and top[y,x]: img[y,x]=(48,51,57,255)
                x+=1; y+=rng.choice([0,1,-1,0])
    for y in range(BH,H):
        for x in range(BW):
            for s in range(1,SL+1):
                yy=y-s
                if 0<=yy<BH and top[yy,x]:
                    left=x<BW/2
                    img[y,x]=(*shade(PAV,.8 if left else .62),255); break
    sil=img[...,3]>0
    out=img.copy()
    for y in range(H):
        for x in range(BW):
            if not sil[y,x]: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                xx,yy=x+dx,y+dy
                if not(0<=xx<BW and 0<=yy<H) or not sil[yy,xx]:
                    out[y,x]=(*OUTL,255); break
    return np.kron(out,np.ones((SC,SC,1),np.uint8)).astype(np.uint8)

def sheet(cells,name):
    h,w=cells[0].shape[:2]
    S=np.zeros((h,w*len(cells),4),np.uint8)
    for i,c in enumerate(cells): S[:,i*w:(i+1)*w]=c
    Image.fromarray(S).save(OUT+name,optimize=True)
    return w,h

if __name__=='__main__':
    info={}
    for st in range(4):
        cells=[render_cell(m,st,1000*st+m) for m in range(16)]
        info['roads_%d'%st]=sheet(cells,'roads_%d.png'%st)
    bc=[];M=0
    for ax in ('x','y'):
        for st in (0,2):
            c,M=bridge_cell(ax,st,77+st); bc.append(c)
    info['bridges']=sheet(bc,'bridges.png'); info['bridge_margin']=M*SC
    pk=[parking_cell(o,s,500+o*3+s) for o in (0,1) for s in (0,1)]
    info['parking']=sheet(pk,'parking.png')
    json.dump(info,open(OUT+'roads_info.json','w'))
    print(info)
