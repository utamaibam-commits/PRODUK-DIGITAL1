from eng import *
V=4; sc,TOTAL=timeline(V)
PAPER=(250,248,240);INK=(30,30,34);TRED=(200,30,40);BG0=(38,42,50)
rng=np.random.default_rng(8)
def mkbg():
    a=np.zeros((H,W,3),np.float32);a[:]=BG0
    y=np.arange(H)[:,None];a+=((np.sin(y/9)*0.5+0.5)*4)[...,None]
    a+=rng.standard_normal((H,W,1)).astype(np.float32)*3
    v=np.linspace(-1,1,W)[None,:]**2*18+np.linspace(-1,1,H)[:,None]**2*18; a-=v[...,None]
    im=Image.fromarray(a.clip(0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([50,180,1030,280],30,fill=(18,20,24)); d.rectangle([75,248,1005,262],fill=(5,5,6))
    d.text((100,200),'KASIR · KasRapi',font=F('mono',30,'Bold'),fill=(120,126,140))
    d.ellipse([960,205,985,230],fill=(60,220,120))
    return im
BG=mkbg()
PX0,PX1=90,990
IS=lambda im:(PX1-PX0-50)/im.width
def mono(txt,size=46,w='Bold',col=INK): return tsprite(txt,F('mono',size,w),col)
def staple(d,x,y):
    d.rectangle([x-40,y-6,x+40,y+6],fill=(150,155,165)); d.rectangle([x-40,y-6,x+40,y-2],fill=(200,205,215))
TRX=card(shot('kasrapi-transaksi',160,470),r=12,shadow_op=60,blur=10,off=(0,6))
STK=card(shot('kasrapi-stok',110,262),r=12,shadow_op=60,blur=10,off=(0,6))
KAN=card(shot('kasrapi-laporan',690,1062),r=12,shadow_op=60,blur=10,off=(0,6))
LAPB=card(shot('kasrapi-laporan',60,230),r=12,shadow_op=60,blur=10,off=(0,6))
def items(i,b):
    # list of (t_appear, kind, payload, height)
    L=[]
    if i==0:
        L=[(b[0],'c',('*** STRUK JUALAN ***',44),80),(b[0]+0.3,'dash',None,40),
           (b[0]+0.5,'kv',('SHOPEE','1x'),70),(b[0]+0.9,'kv',('TIKTOK SHOP','1x'),70),(b[0]+1.3,'kv',('WHATSAPP','1x'),70),
           (b[1],'dash',None,40),(b[1]+0.2,'kv',('POTONGAN','???'),70),(b[1]+0.6,'kv',('LABA','???'),70)]
    elif i==1:
        L=[(b[0],'c',('KasRapi',64),90),(b[0]+0.3,'c',('CATAT PER KANAL',40),60),(b[0]+0.5,'dash',None,40),
           (b[1]-0.1,'img',TRX,TRX.height*IS(TRX)+20),(b[2],'kv',('POTONGAN','DIHITUNG'),70),(b[2]+0.5,'kv',('MARGIN','AKURAT'),70)]
    elif i==2:
        L=[(b[0],'c',('-- STOK --',56),90),(b[0]+0.4,'kv',('TERJUAL','1 pcs'),70),(b[0]+0.8,'kv',('STOK','-1 OTOMATIS'),70),(b[0]+1.1,'dash',None,40),
           (b[0]+1.3,'img',STK,STK.height*IS(STK)+20),(b[1],'red',('! STOK MENIPIS = KETAHUAN',40),80)]
    elif i==3:
        L=[(b[0],'c',('KANAL PALING CUAN?',48),90),(b[0]+0.6,'dash',None,40),(b[0]+0.8,'img',KAN,KAN.height*IS(KAN)+20),(b[1]+0.3,'red',('>> LABA BERSIH PER KANAL',38),80)]
    elif i==4:
        L=[(b[0],'c',('LAPORAN',64),90),(b[0]+0.4,'img',LAPB,LAPB.height*IS(LAPB)+20),(b[0]+1.3,'kv',('CETAK PDF','OK'),70),(b[0]+1.8,'kv',('KIRIM WHATSAPP','OK'),70)]
    else:
        L=[(b[0],'c',('KasRapi',90),120),(b[0]+0.3,'c',('kas · stok · laba bersih',34),60),(b[0]+0.5,'dash',None,40),
           (b[0]+0.7,'kv',('1x APLIKASI','Rp59.000'),70),(b[0]+1.0,'dash',None,40),(b[0]+1.2,'big',('TOTAL','Rp59.000'),100),
           (b[1],'bar',None,130),(b[1]+0.4,'red',('CEK LINK DI BIO',52),80),(b[1]+0.7,'c',('lynk.id/ibam2178',46),70),(b[1]+1.0,'c',('terima kasih :)',34),60)]
    return L
def draw(t):
    s=scene_at(sc,t); lt=t-s['start']; b=s['beats']; i=s['i']
    cv=BG.copy()
    L=items(i,b); y=290; shown=[]
    for (ta,k,pl,h) in L:
        if t>=ta: shown.append((ta,k,pl,h,y)); y+=h
        else: break
    bottom=y+30
    # paper animate height (ease)
    if shown:
        last=shown[-1]; prog=eo((t-last[0])/0.35); prevb=last[4]+30
        bottom=prevb+(last[3])*prog
    else: bottom=280
    paper=Image.new('RGBA',(PX1-PX0,int(bottom-250)+40),PAPER+(255,)); pd=ImageDraw.Draw(paper)
    # torn edge
    zz=[(x, paper.height-40+ (14 if (x//20)%2 else 0)) for x in range(0,paper.width+20,20)]
    pd.polygon([(0,paper.height-40)]+zz+[(paper.width,paper.height),(0,paper.height)],fill=(0,0,0,0))
    pd.polygon([(0,0),(paper.width,0),(paper.width,paper.height-40)]+zz[::-1]+[(0,paper.height-40)],fill=PAPER+(255,))
    pw=paper.width
    for (ta,k,pl,h,yy) in shown:
        yy=yy-250; a=clamp((t-ta)/0.12)
        if k=='c': sp=mono(pl[0],pl[1]); paper.alpha_composite(sp,(int(pw/2-sp.width/2),int(yy+h/2-sp.height/2)))
        elif k=='red': sp=mono(pl[0],pl[1],'ExtraBold',TRED); paper.alpha_composite(sp,(int(pw/2-sp.width/2),int(yy+h/2-sp.height/2)))
        elif k=='dash': pd.line([(30,yy+h/2),(pw-30,yy+h/2)],fill=(150,150,150),width=3)
        elif k=='kv':
            a1=mono(pl[0],42,'Medium'); a2=mono(pl[1],42,'ExtraBold')
            paper.alpha_composite(a1,(36,int(yy+12))); paper.alpha_composite(a2,(int(pw-36-a2.width),int(yy+12)))
            pd.line([(46+a1.width,yy+44),(pw-50-a2.width,yy+44)],fill=(190,190,190),width=2)
        elif k=='big':
            a1=mono(pl[0],60,'ExtraBold'); a2=mono(pl[1],60,'ExtraBold')
            paper.alpha_composite(a1,(36,int(yy+14))); paper.alpha_composite(a2,(int(pw-36-a2.width),int(yy+14)))
        elif k=='bar':
            r=np.random.default_rng(1);x=80
            while x<pw-80:
                w_=int(r.integers(3,12)); pd.rectangle([x,yy+10,x+w_,yy+h-20],fill=INK); x+=w_+int(r.integers(4,10))
        elif k=='img':
            sc_=IS(pl)
            im=pl.resize((int(pl.width*sc_),int(pl.height*sc_)),Image.LANCZOS)
            paper.alpha_composite(im,(int(pw/2-im.width/2),int(yy)))
            staple(pd,pw/2,yy+14)
    # paper scroll: if too long, shift up
    off=max(0,bottom-1560)
    # print shake
    sh=0
    if shown and t-shown[-1][0]<0.35: sh=math.sin(t*90)*2
    cv.paste(paper.convert('RGB'),(int(PX0+sh),int(255-off)),paper.getchannel('A'))
    d=ImageDraw.Draw(cv); d.rounded_rectangle([50,180,1030,280],30,fill=(18,20,24)); d.rectangle([75,248,1005,262],fill=(5,5,6))
    d.text((100,200),'KASIR · KasRapi',font=F('mono',30,'Bold'),fill=(120,126,140)); d.ellipse([960,205,985,230],fill=(60,220,120) if int(t*4)%2 else (30,120,70))
    paste(cv,tsprite('@klisacom',F('mono',32,'Bold'),(150,156,170)),(W/2,130))
    if i==0 and len(b)>2 and t>b[2]:
        p=t-b[2]; im=Image.new('RGBA',(520,200),(0,0,0,0)); dd=ImageDraw.Draw(im)
        dd.rounded_rectangle([6,6,513,193],20,outline=TRED+(255,),width=12); im.alpha_composite(tsprite('RIBET!',F('mono',120,'ExtraBold'),TRED),(70,30))
        paste(cv,im,(W/2,1100),scale=1+0.6*max(0,1-p/0.15),angle=12,alpha=0.92)
    if i in (1,2,3,4) and shown and any(k=='img' for (_,k,_,_,_) in shown):
        paste(cv,tsprite('*data contoh',F('mono',28,'Medium'),(170,176,190)),(900,1640))
    if i>0 and lt<0.22:
        a=1-lt/0.22; cv=Image.blend(cv,Image.new('RGB',(W,H),(250,248,240)),a*0.7)
    return cv
def events():
    ev=[];S=sc
    for s in S:
        if s['i']>0: ev.append((s['start'],'whoosh'))
        for (ta,k,pl,h) in items(s['i'],s['beats']):
            ev.append((ta,'print' if k in('kv','c','dash','big','bar') else ('stamp' if k=='img' else 'pop')))
    ev.append((S[0]['beats'][2],'stamp')); ev.append((S[0]['beats'][2]+0.05,'err'))
    ev.append((S[5]['beats'][0]+1.2,'ding')); ev.append((S[5]['beats'][-1]+0.7,'ding'))
    return ev
if __name__=='__main__': main(V,draw,events,'receipt',100,'v4-kasrapi-strukkasir',sc,TOTAL)
