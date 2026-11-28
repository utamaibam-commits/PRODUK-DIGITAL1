from eng import *
V=1; sc,TOTAL=timeline(V)
PAPER=(241,234,218);INK=(28,24,20);RED=(200,30,36);MUT=(110,100,88)
def mkbg():
    a=np.array(Image.new('RGB',(W,H),PAPER)).astype(np.float32)
    a+=grain(3,9); y=np.linspace(-1,1,H)[:,None]; x=np.linspace(-1,1,W)[None,:]
    a*= (1-0.10*(x**2+y**2))[...,None]
    im=Image.fromarray(a.clip(0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    ttext(d,(W/2,190),'Kabar Warung',F('frak',150),INK)
    d.line([60,280,W-60,280],fill=INK,width=6); d.line([60,292,W-60,292],fill=INK,width=2)
    ttext(d,(60,318),'SENIN, 30 NOVEMBER 2026',F('old',30),INK,'lm'); ttext(d,(W-60,318),'EDISI UMKM  ·  @klisacom',F('old',30),INK,'rm')
    d.line([60,345,W-60,345],fill=INK,width=2)
    d.line([60,H-150,W-60,H-150],fill=INK,width=2)
    ttext(d,(W/2,H-110),'Simpan & bagikan ke sesama pedagang',F('old',30),MUT)
    return im
BG=mkbg()
def headline(cv,lines,t0,t,y=470,size=120,color=INK,lh=1.02):
    p=t-t0
    if p<0: return y
    f=F('old',size)
    for k,l in enumerate(lines):
        q=p-k*0.12
        if q<0: break
        s=lerp(1.35,1,eo(q/0.22)); a=eo(q/0.15)
        paste(cv,tsprite(l,f,color),(W/2,y+k*size*lh),scale=s,alpha=a)
    return y+len(lines)*size*lh
def body(d,text,t0,t,y,size=46,maxw=900,color=INK):
    if t<t0: return
    f=F('play',size); ls=wrap(text,f,maxw); n=int(clamp((t-t0)/1.2)*sum(len(l) for l in ls))
    for k,l in enumerate(ls):
        s=l[:max(0,n)]; n-=len(l)
        ttext(d,(W/2,y+k*size*1.35),s,f,color,'mm' if False else 'mt') if False else d.text((W/2-f.getlength(l)/2,y+k*size*1.35),s,font=f,fill=color)
def circle(d,box,t0,t,dur=0.5,col=RED,w=9):
    p=clamp((t-t0)/dur)
    if p<=0: return
    x0,y0,x1,y1=box; cx,cy=(x0+x1)/2,(y0+y1)/2; rx,ry=(x1-x0)/2,(y1-y0)/2
    pts=[(cx+rx*math.cos(a)*(1+0.03*math.sin(3*a)),cy+ry*math.sin(a)) for a in np.linspace(-2.6,-2.6+2*math.pi*1.08*p,90)]
    d.line(pts,fill=col,width=w,joint='curve')
def stamp(cv,text,cx,cy,t0,t,ang=-12,size=70):
    p=t-t0
    if p<0: return
    sp=tsprite(text,F('archivo',size),RED); im=Image.new('RGBA',(sp.width+60,sp.height+40),(0,0,0,0))
    dd=ImageDraw.Draw(im); dd.rounded_rectangle([3,3,im.width-4,im.height-4],12,outline=RED,width=7); im.alpha_composite(sp,(30,20))
    paste(cv,im,(cx,cy),scale=lerp(2.2,1,eo(p/0.18)),angle=ang,alpha=min(1,p/0.1)*0.92)
def box(d,x0,y0,x1,y1,w=4): d.rectangle([x0,y0,x1,y1],outline=INK,width=w)
def icon_money(d,cx,cy,s,col):
    d.rounded_rectangle([cx-s,cy-s*0.55,cx+s,cy+s*0.55],18,outline=col,width=8); d.ellipse([cx-s*0.3,cy-s*0.3,cx+s*0.3,cy+s*0.3],outline=col,width=8)
NOTA=card(shot('kasrapi-laporan',150,560),r=20,shadow_op=60,blur=20)
HOME=phone('kasrapi-beranda',0,700,w=520)
def draw(t):
    s=scene_at(sc,t); lt=t-s['start']; b=s['beats']; i=s['i']
    cv=BG.copy(); d=ImageDraw.Draw(cv)
    # page slide in
    if i==0:
        y=headline(cv,['WARUNG RAMAI,','UANG RAIB?'],0.03,t,540,112)
        ttext(d,(W/2,800),'Pedagang heran: omzet jalan, laci tetap kosong',F('play',44),MUT) if t>b[1] else None
        circle(d,(250,600,830,720),b[2],t)
        if t>b[1]+0.2:
            for k in range(3):
                q=appear(t,b[1]+0.2+k*0.25); cx=230+k*310; cy=1180
                box(d,cx-130,cy-170,cx+130,cy+170,4)
                if q>0:
                    icon_money(d,cx,cy-30,80*q,INK)
                    ttext(d,(cx,cy+110),['Laci','Dompet','Dapur'][k],F('old',42),INK)
            if t>b[3]: stamp(cv,'KE MANA?',W/2,1400,b[3],t,-8,90)
        body(d,'Warung rame tiap hari, tapi pas dihitung, duitnya nggak ada.',b[0]+0.4,t,1560,40)
    else:
        num=['','PENYEBAB #1','PENYEBAB #2','PENYEBAB #3','SOLUSINYA','IKLAN'][i]
        if i<5:
            ttext(d,(W/2,420),num,F('archivo',54),RED) if t>b[0] else None
            d.line([300,460,W-300,460],fill=RED,width=4) if t>b[0] else None
        if i==1:
            headline(cv,['UANG JUALAN','KECAMPUR','UANG DAPUR'],b[0],t,560,118)
            # two jars mixing
            q=clamp((t-b[1])/1.4); 
            for k,(lab,col) in enumerate([('JUALAN',INK),('DAPUR',RED)]):
                cx=lerp(330+k*420,W/2+(k-0.5)*120,eio(q)); cy=1150
                d.rounded_rectangle([cx-150,cy-180,cx+150,cy+180],30,outline=col,width=8); ttext(d,(cx,cy),lab,F('old',52),col)
            if t>b[-1]: stamp(cv,'BOLONG!',W/2,1450,b[-1],t,8,96)
        elif i==2:
            headline(cv,['KASBON','PELANGGAN','TAK DICATAT'],b[0],t,560,124)
            for k,(nm,am) in enumerate([('Pak Joko','Rp45.000'),('Bu Sri','Rp28.000'),('Mas Andi','Rp60.000')]):
                q=appear(t,b[1]+k*0.3)
                if q>0:
                    y=1040+k*120; d.line([200,y+45,880,y+45],fill=MUT,width=2)
                    d.text((210,y),nm,font=F('play',50),fill=INK); d.text((880-F('play',50).getlength(am),y),am,font=F('play',50),fill=INK)
                    if t>b[2]+k*0.2: ttext(d,(930,y+28),'?',F('archivo',70),RED)
            if t>b[-1]: stamp(cv,'IKHLAS??',W/2,1500,b[-1],t,-8,90)
        elif i==3:
            headline(cv,['CUMA LIHAT','OMZET, BUKAN','LABA BERSIH'],b[0],t,560,118)
            if t>b[1]:
                q=clamp((t-b[1])/1.0)
                for k,(lab,v,col) in enumerate([('OMZET',1.0,INK),('LABA',0.25,RED)]):
                    x=300+k*480; hh=520*v*eo(q); d.rectangle([x-90,1500-hh,x+90,1500],fill=col)
                    ttext(d,(x,1545),lab,F('old',46),INK)
                d.line([150,1500,930,1500],fill=INK,width=5)
            circle(d,(200,760,880,900),b[2],t)
        elif i==4:
            headline(cv,['3 LANGKAH','BIAR UANG','NGGAK RAIB'],b[0],t,560,118)
            for k,txt in enumerate(['Pisahkan kas usaha','Catat setiap kasbon','Cek laba tiap hari']):
                q=appear(t,b[min(k+1,len(b)-1)]-0.1)
                if q>0:
                    y=1020+k*150; box(d,170,y-40,250,y+40,6)
                    if q>0.5: d.line([(185,y),(205,y+25),(240,y-30)],fill=RED,width=12)
                    d.text((290,y-34),txt,font=F('play',60),fill=INK)
            if t>b[-1]: stamp(cv,'SIMPAN!',W/2,1520,b[-1],t,-6,90)
        elif i==5:
            ttext(d,(W/2,420),'— IKLAN —',F('old',40),MUT) if t>b[0] else None
            headline(cv,['KasRapi'],b[0],t,520,150,RED)
            ttext(d,(W/2,640),'Buku kas, stok & laba bersih otomatis',F('play',44),INK) if t>b[0]+0.3 else None
            q=appear(t,b[0]+0.3,0.5); paste(cv,HOME,(W/2,1060+(1-q)*200),scale=0.68,alpha=q)
            if t>b[1]:
                box(d,140,1490,940,1700,6); ttext(d,(W/2,1555),'LINK DI PROFIL',F('archivo',64),INK); ttext(d,(W/2,1640),'Komen "MAU" buat lihat demonya',F('play',42),RED)
            if t>b[-1]: stamp(cv,'Rp59RB SEKALI BAYAR',W/2,1400,b[-1],t,-5,52)
    # page turn wipe at scene start
    if lt<0.25 and i>0:
        x=int(W*(1-eio(lt/0.25))); d.rectangle([0,0,x,H],fill=PAPER); d.line([x,0,x,H],fill=MUT,width=4)
    return cv
def events():
    ev=[]
    for s in sc:
        b=s['beats']; i=s['i']
        if i>0: ev.append((s['start'],'swish'))
        ev.append((b[0],'print' if i in (0,5) else 'thump'))
        if i in(1,2,3,4) and len(b)>1: ev+= [(b[1],'pop')]
        ev.append((b[-1],'stamp'))
    ev.append((sc[-1]['beats'][-1]+0.6,'ding'))
    return ev
main(V,draw,events,'news',100,'v1-koran',sc,TOTAL)
