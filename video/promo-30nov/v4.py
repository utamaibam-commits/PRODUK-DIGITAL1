from eng import *
V=4; sc,TOTAL=timeline(V)
GR=(24,120,72);LG=(232,245,236);GRID=(214,218,222);INK=(30,34,38);MUT=(120,126,132);RED=(214,48,49);WHITE=(255,255,255)
X0,XA,XB,X1=40,130,600,1040; Y0=560; RH=104
def mkbg():
    im=Image.new('RGB',(W,H),(246,247,248)); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,250],fill=GR); d.text((60,70),'Hitung-Laba-Warung',font=F('inter',54,'Bold'),fill=WHITE); d.text((60,150),'File   Edit   Lihat   Sisipkan   Format',font=F('inter',32,'Regular'),fill=(200,235,215))
    d.rectangle([0,250,W,380],fill=WHITE); d.line([0,380,W,380],fill=GRID,width=3)
    d.rounded_rectangle([40,280,150,350],10,fill=(240,240,240)); ttext(d,(95,315),'fx',F('inter',40,'Bold'),MUT)
    d.rectangle([X0,440,X1,Y0],fill=(238,240,242)); 
    for x,l in [((XA+XB)/2,'A'),((XB+X1)/2,'B')]: ttext(d,(x,Y0-50),l,F('inter',40,'SemiBold'),MUT)
    for r in range(11):
        y=Y0+r*RH; d.line([X0,y,X1,y],fill=GRID,width=2)
        if r<10: d.rectangle([X0,y+1,XA,y+RH-1],fill=(238,240,242)); ttext(d,((X0+XA)/2,y+RH/2),str(r+1),F('inter',34,'Medium'),MUT)
    for x in (X0,XA,XB,X1): d.line([x,440,x,Y0+10*RH],fill=GRID,width=2)
    d.text((60,H-140),'@klisacom  ·  KasRapi',font=F('inter',36,'SemiBold'),fill=MUT)
    return im
BG=mkbg()
def typed(s,t0,t,cps=22):
    if t<t0: return ''
    return s[:int((t-t0)*cps)+1]
def cell(d,r,col,text,color=INK,bold=False,fill=None):
    y=Y0+r*RH
    if fill: d.rectangle([XA+2 if col=='A' else XB+2,y+2,(XB-2 if col=='A' else X1-2),y+RH-2],fill=fill)
    f=F('inter',50,'Bold' if bold else 'Medium')
    if col=='A': d.text((XA+28,y+RH/2),text,font=f,fill=color,anchor='lm')
    else: d.text((X1-28,y+RH/2),text,font=f,fill=color,anchor='rm')
def sel(d,r,col,t0,t):
    if t<t0: return
    y=Y0+r*RH; x0,x1=(XA,XB) if col=='A' else (XB,X1)
    d.rectangle([x0,y,x1,y+RH],outline=GR,width=7); d.rectangle([x1-12,y+RH-12,x1+4,y+RH+4],fill=GR)
def fbar(d,text):
    d.text((180,315),text,font=F('mono',44,'Bold'),fill=INK,anchor='lm')
def callout(cv,text,cy,t0,t,bg=INK,fg=WHITE,size=70,ang=-2):
    p=t-t0
    if p<0: return
    f=F('inter',size,'Black')
    while f.getlength(text)>920: size-=3; f=F('inter',size,'Black')
    sp=tsprite(text,f,fg); im=Image.new('RGBA',(sp.width+70,sp.height+46),(0,0,0,0))
    ImageDraw.Draw(im).rounded_rectangle([0,0,im.width-1,im.height-1],22,fill=bg+(255,)); im.alpha_composite(sp,(35,23))
    paste(cv,im,(W/2,cy),scale=0.6+0.4*spring(p*1.3),angle=ang,alpha=eo(p/0.12))
ROWS=[]
LAP=phone('kasrapi-laporan',150,700,w=600)
def rows_upto(d,t,sc_):
    b3=sc[2]['beats'];b4=sc[3]['beats'];b5=sc[4]['beats']
    R=[(0,'Omzet','1.000.000',b3[1],INK),(1,'Modal barang','-600.000',b3[2],RED),(2,'Sisa (laba kotor)','400.000',b3[3],GR),
       (3,'Gas','-40.000',b4[1],RED),(4,'Plastik','-25.000',b4[1]+0.4,RED),(5,'Listrik','-35.000',b4[1]+0.8,RED),(6,'Bensin','-50.000',b4[2]-0.2,RED),(7,'Total biaya','-150.000',b4[2]+0.3,RED)]
    last=None
    for r,a,v,t0,col in R:
        if t>=t0:
            cell(d,r,'A',typed(a,t0,t),INK,r in (2,7)); 
            if t>=t0+0.35: cell(d,r,'B',typed(v,t0+0.35,t),col,r in (2,7))
            last=(r,'B' if t>=t0+0.35 else 'A',t0)
    if t>=b5[0]:
        cell(d,9,'A','LABA BERSIH',WHITE,True,fill=GR); cell(d,9,'B',typed('250.000',b5[0]+0.3,t,10),WHITE,True,fill=GR); last=(9,'B',b5[0])
    return last
def draw(t):
    s=scene_at(sc,t); i=s['i']; b=s['beats']
    cv=BG.copy(); d=ImageDraw.Draw(cv)
    if i==0:
        cell(d,0,'A',typed('Omzet hari ini',0.05,t),INK); cell(d,0,'B',typed('1.000.000',0.45,t),INK,True); sel(d,0,'B',0.45,t)
        cell(d,1,'A',typed('Untung?',b[0]+0.8,t),INK)
        if t>b[0]+1.2: cell(d,1,'B',typed('1.000.000 ???',b[0]+1.2,t),RED,True); sel(d,1,'B',b[0]+1.2,t)
        fbar(d,typed('=B1',0.45,t))
        callout(cv,'OMZET = UNTUNG?',1500,0.05,t,INK,WHITE,90)
        callout(cv,'BELUM TENTU, BESTIE!',1680,b[1],t,RED,WHITE,72,3)
    elif i==1:
        f='=OMZET - MODAL - BIAYA'; fbar(d,typed(f,b[0]+0.3,t,9))
        d.rectangle([X0,440,X1,Y0+10*RH],fill=(246,247,248))
        p=t-b[0]
        if p>0:
            for k,(tx,col) in enumerate([('LABA BERSIH',GR),('=',INK),('OMZET',INK),('- MODAL BARANG',RED),('- BIAYA OPERASIONAL',RED)]):
                q=appear(t,b[min(k,len(b)-1)] if k<4 else b[-1]+0.3)
                if q>0:
                    sz=100 if k!=1 else 120
                    while F('inter',sz,'Black').getlength(tx)>960: sz-=4
                    paste(cv,tsprite(tx,F('inter',sz,'Black'),col),(W/2,620+k*190+(1-q)*60),alpha=q)
        callout(cv,'SIMPAN RUMUSNYA!',1720,b[-1]+0.8,t,GR,WHITE,64)
    else:
        last=rows_upto(d,t,sc)
        if last: sel(d,last[0],last[1],last[2],t)
        if i==2:
            fbar(d,'=B1-B2'); callout(cv,'Sisa Rp400rb',1700,b[-1]+0.4,t,INK,WHITE,70)
        elif i==3:
            fbar(d,'=SUM(B4:B7)'); callout(cv,'Biaya kecil, kalau dijumlah lumayan',1700,b[-1]+0.2,t,RED,WHITE,60)
        elif i==4:
            fbar(d,'=B3+B8')
            p=t-b[1]
            if p>0:
                callout(cv,'Rp250.000 MASUK KANTONG',1720,b[1],t,GR,WHITE,70,-3)
            if t>b[-1]: callout(cv,'ANJAY!',470,b[-1],t,(255,200,0),INK,80,6)
        elif i==5:
            d.rectangle([0,250,W,H],fill=(18,52,36))
            ttext(d,(W/2,360),'KasRapi ngitungin otomatis',F('inter',62,'Black'),WHITE) if t>b[0] else None
            q=appear(t,b[0]+0.1,0.5); paste(cv,LAP,(W/2,1000+(1-q)*300),scale=0.95,alpha=q)
            callout(cv,'Link di profil',1600,b[1],t,(255,200,0),INK,72)
            callout(cv,'Simpan video ini!',1760,b[2],t,WHITE,GR,56,2)
    return cv
def events():
    ev=[(0.05,'click'),(0.45,'click'),(sc[0]['beats'][1],'err')]
    for s in sc[1:]:
        b=s['beats']; ev+=[(s['start'],'swish')]
        ev+=[(x,'click') for x in b]
        ev+=[(x+0.35,'tick') for x in b[1:]]
    ev+=[(sc[4]['beats'][1],'ding'),(sc[4]['beats'][-1],'stamp'),(sc[5]['beats'][1],'pop')]
    for k in range(10): ev.append((sc[1]['beats'][0]+0.3+k*0.25,'tick'))
    return ev
main(V,draw,events,'sheet',96,'v4-sheet',sc,TOTAL)
