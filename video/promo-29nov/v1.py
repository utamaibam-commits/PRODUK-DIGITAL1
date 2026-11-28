from eng import *
V=1; sc,TOTAL=timeline(V)
rng=np.random.default_rng(3)
# board background
def mkbg():
    base=np.zeros((H,W,3),np.float32); base[:]=(30,58,42)
    n=rng.standard_normal((H//8,W//8)).astype(np.float32)
    n=np.array(Image.fromarray(((n*20+128).clip(0,255)).astype(np.uint8)).resize((W,H),Image.BICUBIC)).astype(np.float32)-128
    base+=n[...,None]*0.35
    # smudges
    sm=Image.new('L',(W,H),0);d=ImageDraw.Draw(sm)
    for _ in range(14):
        x,y=rng.integers(0,W),rng.integers(0,H);r=rng.integers(80,260)
        d.ellipse([x-r*1.8,y-r*0.5,x+r*1.8,y+r*0.5],fill=int(rng.integers(10,28)))
    sm=np.array(sm.filter(ImageFilter.GaussianBlur(60))).astype(np.float32)
    base+=sm[...,None]*0.9
    g=rng.standard_normal((H,W)).astype(np.float32)*4; base+=g[...,None]
    im=Image.fromarray(base.clip(0,255).astype(np.uint8))
    d=ImageDraw.Draw(im)
    # wooden frame
    for i,c in enumerate([(92,60,34),(120,80,46),(100,66,38)]):
        d.rectangle([i*8,i*8,W-1-i*8,H-1-i*8],outline=c,width=8)
    # chalk ledge
    d.rectangle([0,H-300,W,H-270],fill=(110,74,42)); d.rectangle([0,H-300,W,H-296],fill=(140,98,60))
    for x,c in [(160,(240,236,220)),(250,(245,215,110)),(330,(242,139,130))]:
        d.rounded_rectangle([x,H-318,x+70,H-300],6,fill=c)
    return im
BG=mkbg()
GRAIN=Image.fromarray((rng.random((H,W))*255).astype(np.uint8))
CREAM=(242,238,222);YEL=(246,214,110);CORAL=(242,139,130);MINT=(160,226,190)
_cc={}
def chalk(text,size,color):
    k=(text,size,color)
    if k in _cc: return _cc[k]
    sp=tsprite(text,F('chalk',size),color).copy()
    a=np.array(sp.getchannel('A')).astype(np.float32)
    g=np.array(GRAIN.crop((0,0,sp.width,sp.height))).astype(np.float32)/255
    a=a*(0.55+0.45*(g>0.25))*(0.85+0.15*g)
    sp.putalpha(Image.fromarray(a.clip(0,255).astype(np.uint8))); _cc[k]=sp; return sp
def write(cv,text,size,color,cx,cy,p,angle=0):
    if p<=0: return
    sp=chalk(text,size,color)
    if p<1:
        w=int(sp.width*eo(p)); 
        if w<2: return
        s2=Image.new('RGBA',sp.size,(0,0,0,0)); s2.paste(sp.crop((0,0,w,sp.height)),(0,0)); sp=s2
    paste(cv,sp,(cx,cy),angle=angle)
def line(d,pts,p,color,w=8):
    if p<=0: return
    L=len(pts)-1; m=p*L
    for i in range(L):
        f=clamp(m-i)
        if f<=0: break
        x0,y0=pts[i];x1,y1=pts[i+1]
        d.line([x0,y0,x0+(x1-x0)*f,y0+(y1-y0)*f],fill=color,width=w)
def ellipse(d,box,p,color,w=7):
    if p<=0: return
    x0,y0,x1,y1=box;cx,cy=(x0+x1)/2,(y0+y1)/2;rx,ry=(x1-x0)/2,(y1-y0)/2
    n=int(80*clamp(p)); pts=[(cx+rx*math.cos(-2.2+i/80*2*math.pi*1.08),cy+ry*math.sin(-2.2+i/80*2*math.pi*1.08)) for i in range(n+1)]
    if len(pts)>1: d.line(pts,fill=color,width=w,joint='curve')
def tape(cv,x,y,ang):
    t=Image.new('RGBA',(120,40),(235,225,190,200)); paste(cv,t,(x,y),angle=ang)
LAP=card(shot('kasrapi-laporan',238,566),r=26,shadow_op=120)
PRIB=card(shot('kasrapi-laporan',568,662),r=26,shadow_op=120)
PRIB2=card(shot('kasrapi-beranda',352,436,196,378),r=22,shadow_op=120)
def wp(t,t0,dur=0.5): return clamp((t-t0)/dur)
def draw(t):
    s=scene_at(sc,t); lt=t-s['start']; b=s['beats']; i=s['i']
    cv=BG.copy(); d=ImageDraw.Draw(cv)
    write(cv,'@klisacom',40,CREAM,W/2,150,1)
    if i==0:
        write(cv,'OMZET GEDE',190,CREAM,W/2,560,wp(t,b[0]-0.05,0.55),-3)
        line(d,[(220,690),(860,675)],wp(t,b[0]+0.5,0.3),YEL,10)
        write(cv,'tapi duitnya...',110,CREAM,W/2,850,wp(t,b[1],0.5))
        sh=math.sin(t*40)*6*clamp(1-(t-b[2])*2) if t>b[2] else 0
        write(cv,'KE MANA??',200,CORAL,W/2+sh,1080,wp(t,b[2],0.45),2)
        for k,(x,y) in enumerate([(180,1300),(880,1260),(760,420)]):
            write(cv,'?',140,YEL,x,y,wp(t,b[2]+0.3+k*0.15,0.2),15*(k-1))
    elif i==1:
        write(cv,'RUMUS CUAN',90,YEL,W/2,330,wp(t,b[0],0.4))
        line(d,[(330,395),(750,390)],wp(t,b[0]+0.4,0.2),YEL,6)
        rows=[('Omzet',CREAM,b[1]),('− potongan marketplace',CORAL,b[2]),('− modal barang',CORAL,b[2]+1.45),('− biaya usaha',CORAL,b[3] if len(b)>3 else b[2]+2.6)]
        for k,(tx,c,t0) in enumerate(rows):
            write(cv,tx,96 if k else 120,c,W/2,560+k*165,wp(t,t0,0.55))
        line(d,[(150,1250),(930,1240)],wp(t,(b[3] if len(b)>3 else b[2]+2.6)+0.7,0.3),CREAM,9)
    elif i==2:
        write(cv,'yang sisa =',90,CREAM,W/2,430,wp(t,b[0],0.35))
        write(cv,'LABA BERSIH',170,YEL,W/2,700,wp(t,b[0]+0.45,0.5),-2)
        ellipse(d,(90,560,990,850),wp(t,b[0]+1.0,0.5),CREAM,8)
        write(cv,'bukan omzet ya,',96,CORAL,W/2,1010,wp(t,b[0]+1.75,0.4))
        write(cv,'bestie!',120,CORAL,W/2,1140,wp(t,b[0]+2.2,0.3),-4)
    elif i==3:
        write(cv,'KasRapi ngitung sendiri',92,YEL,W/2,270,wp(t,b[0],0.5))
        p=spring((t-b[0]-0.35)*1.2)
        if p>0:
            sc_=0.8*(0.6+0.4*p); paste(cv,LAP,(W/2,840),scale=sc_,angle=-2)
            tape(cv,W/2-330,840-LAP.height*sc_/2+20,25); tape(cv,W/2+330,840-LAP.height*sc_/2+20,-25)
        if len(b)>1:
            line(d,[(980,1300),(1000,1230),(900,1180)],wp(t,b[1],0.4),CORAL,9)
            line(d,[(900,1180),(940,1170)],wp(t,b[1]+0.4,0.1),CORAL,9);line(d,[(900,1180),(925,1215)],wp(t,b[1]+0.4,0.1),CORAL,9)
            write(cv,'otomatis!',100,CORAL,770,1340,wp(t,b[1]+0.2,0.4),-5)
        write(cv,'*data contoh',40,CREAM,880,1450,1 if p>0.5 else 0)
    elif i==4:
        write(cv,'uang pribadi',100,CREAM,W/2,300,wp(t,b[0],0.4))
        write(cv,'ikut kecatat',100,YEL,W/2,420,wp(t,b[0]+0.4,0.4))
        p=spring((t-b[0]-0.5)*1.2)
        if p>0: paste(cv,PRIB2,(W/2,640),scale=0.9*(0.6+0.4*p),angle=2)
        p2=spring((t-b[0]-0.9)*1.2)
        if p2>0: paste(cv,PRIB,(W/2,880),scale=0.88*(0.6+0.4*p2),angle=-1.5)
        if len(b)>1:
            write(cv,'AMAN',110,MINT,300,1170,wp(t,b[1],0.3)); write(cv,'KEBABLASAN',90,CORAL,740,1170,wp(t,b[1]+0.5,0.4))
            d.rounded_rectangle([170,1100,430,1250],20,outline=MINT,width=6) if t>b[1]+0.2 else None
            if t>b[1]+0.2: d.rounded_rectangle([530,1100,960,1250],20,outline=CORAL,width=6)
            line(d,[(190,1310),(260,1370),(400,1260)],wp(t,b[1]+1.1,0.35),MINT,12)
            write(cv,'yang mana kamu?',60,CREAM,W/2,1430,wp(t,b[1]+1.5,0.4))
    else:
        write(cv,'KasRapi',230,CREAM,W/2,470,wp(t,b[0]-0.05,0.5),-3)
        write(cv,'kas • stok • laba bersih',70,MINT,W/2,660,wp(t,b[0]+0.4,0.4))
        write(cv,'Rp59.000',150,YEL,W/2,850,wp(t,b[0]+0.7,0.4))
        ellipse(d,(240,760,840,950),wp(t,b[0]+1.1,0.45),YEL,7)
        write(cv,'cek link di bio',110,CORAL,W/2,1080,wp(t,b[1],0.45),-2)
        p=wp(t,b[1]+0.5,0.4)
        if p>0:
            d.rounded_rectangle([150,1190,930,1330],24,outline=CREAM,width=6)
            write(cv,'lynk.id/ibam2178',80,CREAM,W/2,1262,p)
    # eraser wipe at scene start
    if i>0 and lt<0.35:
        x=int(lerp(-300,W+300,lt/0.35)); ov=Image.new('L',(W,H),0); od=ImageDraw.Draw(ov)
        od.rectangle([x-260,0,x+260,H],fill=70); ov=ov.filter(ImageFilter.GaussianBlur(50))
        cv=Image.composite(Image.new('RGB',(W,H),(200,210,200)),cv,ov)
    # camera punch
    z=1.0
    for bt in s['beats']:
        if 0<=t-bt<0.4: z=max(z,1+0.025*(1-(t-bt)/0.4))
    if z>1:
        cw,ch=W/z,H/z; cv=cv.resize((W,H),Image.BILINEAR,box=((W-cw)/2,(H-ch)/2,(W+cw)/2,(H+ch)/2))
    return cv
def events():
    ev=[]
    for s in sc:
        b=s['beats']
        if s['i']>0: ev.append((s['start'],'whoosh'))
        for x in b: ev.append((x,'chalk'))
    sc0=sc
    ev+= [(sc0[0]['beats'][2],'thump'),(sc0[2]['beats'][0]+1.0,'chalk'),(sc0[2]['beats'][0]+2.2,'pop'),(sc0[3]['beats'][0]+0.35,'stamp'),(sc0[4]['beats'][0]+0.5,'pop'),(sc0[4]['beats'][0]+0.9,'pop'),(sc0[4]['beats'][-1]+1.1,'ding'),(sc0[5]['beats'][0],'thump'),(sc0[5]['beats'][0]+1.1,'chalk'),(sc0[5]['beats'][-1]+0.5,'ding')]
    ev+= [(sc0[1]['beats'][2]+1.45,'chalk')]
    return ev
if __name__=='__main__': main(V,draw,events,'chalk',96,'v1-kasrapi-papankapur',sc,TOTAL)
