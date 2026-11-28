import json, math, os, subprocess, wave, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W,H,FPS=1080,1920,30
BASE=os.path.dirname(os.path.abspath(__file__))
BE=json.load(open(f'{BASE}/vo/p/beats.json'))
FONTS={'inter':'/usr/share/fonts/opentype/inter/Inter-{w}.otf','mono':'/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-{w}.ttf',
 'anton':f'{BASE}/fonts/Anton-Regular.ttf','chalk':f'{BASE}/fonts/CaveatBrush-Regular.ttf','fred':f'{BASE}/fonts/Fredoka.ttf','serif':f'{BASE}/fonts/DMSerifDisplay-Regular.ttf'}
_fc={}
def F(name,size,w='Bold'):
    k=(name,size,w)
    if k not in _fc:
        p=FONTS[name].format(w=w)
        if not os.path.exists(p): p=FONTS[name].format(w='Bold')
        f=ImageFont.truetype(p,size)
        if name=='fred':
            try: f.set_variation_by_name(w if w!='Bold' else 'Bold')
            except Exception: pass
        _fc[k]=f
    return _fc[k]
def clamp(x,a=0,b=1): return max(a,min(b,x))
def spring(t):
    if t<=0: return 0.0
    return 1-math.exp(-7*t)*math.cos(12*t)
def eo(t): t=clamp(t); return 1-(1-t)**3
def eio(t): t=clamp(t); return t*t*(3-2*t)
def lerp(a,b,t): return a+(b-a)*t

def timeline(v,extra=None):
    sc=[];t=0.0
    for s in range(1,7):
        b=BE[f'v{v}_s{s}']; d=0.3+b['dur']+0.55
        if s==6: d+=1.6
        if extra and s in extra: d+=extra[s]
        sc.append(dict(i=s-1,start=t,dur=d,vo=t+0.3,beats=[t+0.3+x for x in b['beats']],vodur=b['dur']))
        t+=d
    return sc,t
def scene_at(sc,t):
    for s in sc:
        if t<s['start']+s['dur']: return s
    return sc[-1]

_shots={}
def shot(name,y0,y1,x0=0,x1=390):
    k=(name,y0,y1,x0,x1)
    if k not in _shots:
        im=Image.open(f'{BASE}/shots/{name}.png').convert('RGB')
        _shots[k]=im.crop((x0*3,y0*3,x1*3,y1*3))
    return _shots[k]
def fit(im,w=None,h=None):
    if w and not h: h=round(im.height*w/im.width)
    if h and not w: w=round(im.width*h/im.height)
    return im.resize((int(w),int(h)),Image.LANCZOS)
def rmask(size,r):
    m=Image.new('L',size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,size[0]-1,size[1]-1],r,fill=255); return m
def rounded(im,r):
    im=im.convert('RGBA'); im.putalpha(rmask(im.size,r)); return im
def paste(canvas,im,xy,scale=1.0,angle=0.0,alpha=1.0,center=True):
    """paste RGBA/RGB sprite; xy is center if center else top-left"""
    if im.mode!='RGBA': im=im.convert('RGBA')
    if scale!=1.0:
        nw,nh=max(1,int(im.width*scale)),max(1,int(im.height*scale)); im=im.resize((nw,nh),Image.BILINEAR)
    if angle: im=im.rotate(angle,resample=Image.BICUBIC,expand=True)
    if alpha<1.0:
        a=im.getchannel('A').point(lambda p:int(p*alpha)); im.putalpha(a)
    x,y=xy
    if center: x,y=int(x-im.width/2),int(y-im.height/2)
    canvas.paste(im.convert('RGB'),(int(x),int(y)),im.getchannel('A'))
_tc={}
def tsprite(text,font,fill,stroke=0,sfill=None,spacing=0):
    k=(text,id(font),fill,stroke,sfill)
    if k in _tc: return _tc[k]
    bb=font.getbbox(text,stroke_width=stroke)
    w,h=bb[2]-bb[0]+8,bb[3]-bb[1]+8
    im=Image.new('RGBA',(w,h),fill+(0,) if isinstance(fill,tuple) and len(fill)==3 else (0,0,0,0))
    d=ImageDraw.Draw(im); d.text((4-bb[0],4-bb[1]),text,font=font,fill=fill,stroke_width=stroke,stroke_fill=sfill)
    _tc[k]=im; return im
def shadow(im,blur=24,off=(0,18),op=90,color=(0,0,0)):
    a=im.getchannel('A'); pad=blur*2
    s=Image.new('RGBA',(im.width+pad*2,im.height+pad*2),color+(0,))
    m=Image.new('L',s.size,0); m.paste(a.point(lambda p:p*op//255),(pad,pad)); m=m.filter(ImageFilter.GaussianBlur(blur))
    s.putalpha(m); return s,pad
def card(im,r=28,shadow_op=80,blur=26,off=(0,22),border=None):
    im=rounded(im,r)
    if border:
        b=Image.new('RGBA',(im.width+border[0]*2,im.height+border[0]*2),(0,0,0,0))
        ImageDraw.Draw(b).rounded_rectangle([0,0,b.width-1,b.height-1],r+border[0],fill=border[1]+(255,))
        b.alpha_composite(im,(border[0],border[0])); im=b
    s,pad=shadow(im,blur,off,shadow_op)
    out=Image.new('RGBA',(s.width,s.height+abs(off[1])),(0,0,0,0))
    out.alpha_composite(s,(max(0,off[0]),max(0,off[1])))
    out.alpha_composite(im,(pad,pad))
    return out

# ---------------- audio ----------------
SR=44100
def _env(n,a=0.003,d=0.2):
    t=np.arange(n)/SR; return np.minimum(1,t/a)*np.exp(-t/d)
def sfx(kind,seed=0):
    r=np.random.default_rng(seed)
    if kind=='thump':
        n=int(0.45*SR);t=np.arange(n)/SR;f=48+110*np.exp(-t*18);ph=2*np.pi*np.cumsum(f)/SR
        return np.sin(ph)*_env(n,0.002,0.16)*1.0
    if kind=='whoosh':
        n=int(0.5*SR);x=r.standard_normal(n);y=np.zeros(n);a=0
        cut=np.linspace(0.02,0.35,n)**1.5
        for i in range(n): a+= cut[i]*(x[i]-a); y[i]=a
        e=np.sin(np.linspace(0,np.pi,n))**2; return y*e*1.6
    if kind=='tick':
        n=int(0.06*SR);t=np.arange(n)/SR; return np.sin(2*np.pi*2400*t)*_env(n,0.0005,0.012)*0.6
    if kind=='pop':
        n=int(0.15*SR);t=np.arange(n)/SR;f=500+900*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*_env(n,0.001,0.05)*0.8
    if kind=='ding':
        n=int(0.9*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1976*t)+0.3*np.sin(2*np.pi*2637*t))*_env(n,0.002,0.3)*0.45
    if kind=='err':
        n=int(0.35*SR);t=np.arange(n)/SR;return np.sign(np.sin(2*np.pi*110*t))*_env(n,0.003,0.12)*0.35
    if kind=='chalk':
        n=int(0.32*SR);x=r.standard_normal(n);x=np.diff(np.concatenate([[0],x]))
        am=(0.5+0.5*np.sin(2*np.pi*38*np.arange(n)/SR+r.random()*6))**2
        return x*am*np.sin(np.linspace(0,np.pi,n))*0.35
    if kind=='stamp':
        a=sfx('thump',seed);n=int(0.08*SR);c=r.standard_normal(n)*_env(n,0.0005,0.02)*0.7
        a[:n]+=c; return a*1.1
    if kind=='print':
        n=int(0.6*SR);t=np.arange(n)/SR;x=r.standard_normal(n)*(0.5+0.5*np.sign(np.sin(2*np.pi*55*t)))
        return x*0.18*np.minimum(1,t/0.01)*np.minimum(1,(0.6-t)/0.05)
    if kind=='swish':
        a=sfx('whoosh',seed); return a[::2]*0.8
    if kind=='shake':
        n=int(0.7*SR);t=np.arange(n)/SR;x=r.standard_normal(n)*(np.abs(np.sin(2*np.pi*9*t))**4)
        return x*0.35
    if kind=='click':
        n=int(0.03*SR);return r.standard_normal(n)*_env(n,0.0003,0.004)*0.8
    raise ValueError(kind)
def bed(total,bpm,kind,seed=1):
    n=int(total*SR);y=np.zeros(n);beat=60/bpm;r=np.random.default_rng(seed)
    t=np.arange(n)/SR
    roots={'chalk':[220,196,174.6,196],'clean':[261.6,220,174.6,196],'poster':[146.8,130.8,116.5,130.8],'receipt':[196,174.6,164.8,174.6],'warm':[233.1,207.7,174.6,196],'tech':[164.8,146.8,130.8,146.8]}[kind]
    # pad
    for bi,rt in enumerate(roots*20):
        s=int(bi*beat*4*SR); e=min(n,int((bi+1)*beat*4*SR))
        if s>=n: break
        tt=np.arange(e-s)/SR
        ch=sum(np.sin(2*np.pi*rt*m*tt) for m in (1,1.25,1.5))*0.04
        y[s:e]+=ch*np.minimum(1,tt/0.3)
    i=0
    while i*beat<total:
        s=int(i*beat*SR)
        if kind!='clean' or i%2==0:
            k=sfx('thump',i)[: int(0.3*SR)]*0.55; e=min(n,s+len(k)); y[s:e]+=k[:e-s]
        hs=int((i+0.5)*beat*SR); h=r.standard_normal(int(0.04*SR))*_env(int(0.04*SR),0.0005,0.01)*0.12
        if hs+len(h)<n: y[hs:hs+len(h)]+=np.diff(np.concatenate([[0],h]))
        i+=1
    return y
def readwav(f):
    w=wave.open(f);a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768;sr=w.getframerate()
    if sr!=SR:
        idx=np.arange(0,len(a)-1,sr/SR); a=np.interp(idx,np.arange(len(a)),a)
    return a
def mix(v,sc,total,events,bedkind,bpm,out):
    n=int((total+0.2)*SR);vo=np.zeros(n);fx=np.zeros(n)
    for s in sc:
        a=readwav(f'{BASE}/vo/p/v{v}_s{s["i"]+1}.wav'); st=int(s['vo']*SR); e=min(n,st+len(a)); vo[st:e]+=a[:e-st]
    for k,(t,kind) in enumerate(events):
        a=sfx(kind,k); st=int(t*SR)
        if st<0 or st>=n: continue
        e=min(n,st+len(a)); fx[st:e]+=a[:e-st]
    b=bed(total+0.2,bpm,bedkind)[:n]
    # duck bed under voice
    env=np.convolve(np.abs(vo),np.ones(2205)/2205,'same'); duck=1-0.55*np.clip(env*12,0,1)
    y=vo*1.0+fx*0.42+b*0.32*duck
    fade=np.ones(n);fl=int(0.6*SR);fade[-fl:]=np.linspace(1,0,fl)
    y=y*fade; pk=np.max(np.abs(y)); y=y/max(pk,1e-6)*0.95 if pk>0.95 else y
    w=wave.open(out,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((y*32767).astype(np.int16).tobytes());w.close()

# ---------------- render ----------------
_draw=None
def _fr(i):
    return _draw(i/FPS).convert('RGB').tobytes()
def render(draw,total,out,frames=None,workers=4):
    global _draw; _draw=draw
    import multiprocessing as mp
    n=int(total*FPS)
    p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    with mp.get_context('fork').Pool(workers) as pool:
        for b in pool.imap(_fr,range(n),chunksize=4): p.stdin.write(b)
    p.stdin.close();p.wait()
def stills(draw,times,out,cols=6):
    ims=[draw(t).convert('RGB').resize((270,480)) for t in times]
    rows=(len(ims)+cols-1)//cols; sh=Image.new('RGB',(270*cols,480*rows),'white')
    for i,im in enumerate(ims): sh.paste(im,((i%cols)*270,(i//cols)*480))
    sh.save(out)
def main(v,draw,events_fn,bedkind,bpm,name,sc,total):
    mode=sys.argv[1] if len(sys.argv)>1 else 'stills'
    if mode=='stills':
        ts=[]
        for s in sc: ts+= [s['start']+0.25, s['beats'][-1]+0.4, s['start']+s['dur']-0.15]
        stills(draw,ts,f'{BASE}/out/{name}-stills.png')
    else:
        os.makedirs(f'{BASE}/out',exist_ok=True)
        mix(v,sc,total,events_fn(),bedkind,bpm,f'{BASE}/out/{name}.wav')
        render(draw,total,f'{BASE}/out/{name}-v.mp4')
        subprocess.run(['ffmpeg','-y','-v','error','-i',f'{BASE}/out/{name}-v.mp4','-i',f'{BASE}/out/{name}.wav','-c:v','copy','-c:a','aac','-b:a','160k','-ar','44100','-shortest',f'{BASE}/out/{name}.mp4'])
        print('done',name)
