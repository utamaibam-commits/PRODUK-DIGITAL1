import sys;sys.path.insert(0,'/tmp/claude-0/kr/build')
import numpy as np, wave, tl
SR=44100;N=int((tl.TOTAL+0.2)*SR);mix=np.zeros(N);sfx=np.zeros(N);mus=np.zeros(N)
rng=np.random.default_rng(3)
def env(n,dec):return np.exp(-np.arange(n)/SR/dec)
def thump():
    n=int(.35*SR);t=np.arange(n)/SR;f=150*np.exp(-t*18)+48;ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*env(n,.12)*1.0+rng.normal(0,1,n)*env(n,.01)*.3
def whoosh(d=.4):
    n=int(d*SR);x=rng.normal(0,1,n);y=np.zeros(n);a=0
    for i in range(n):
        k=0.02+0.5*(i/n);a+=k*(x[i]-a);y[i]=a
    e=np.sin(np.pi*np.arange(n)/n)**2;return y*e*1.6
def pop():
    n=int(.12*SR);t=np.arange(n)/SR;f=500+900*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.04)*.8
def tick():
    n=int(.05*SR);return rng.normal(0,1,n)*env(n,.006)*.6+np.sin(2*np.pi*2200*np.arange(n)/SR)*env(n,.01)*.4
def ding():
    n=int(.7*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1320*t)+.5*np.sin(2*np.pi*1980*t)+.3*np.sin(2*np.pi*2640*t))*env(n,.22)*.45
def err():
    n=int(.32*SR);t=np.arange(n)/SR;return np.sign(np.sin(2*np.pi*140*t))*.35*(t<.13)+np.sign(np.sin(2*np.pi*120*t))*.35*(t>.16)*(t<.3)
SFX=dict(th=thump,wh=whoosh,po=pop,ti=tick,di=ding,er=err)
def add(buf,t,x,g=1):
    i=int(t*SR);x=x[:max(0,len(buf)-i)];buf[i:i+len(x)]+=x*g
ev={1:[(0.35,'th'),(0.77,'th'),(1.19,'th'),('b1','th'),(('b1',.25),'th'),(('b1',.5),'po'),('b2','er'),('b2','th'),(('b2',.2),'po'),('b3','po'),(('b3',.25),'th'),(('b3',.3),'wh')],
2:[(0.05,'ti'),(0.1,'th'),(0.35,'th'),(0.2,'wh'),('b1','ti'),(('b1',.1),'po'),('b2','po'),(('b2',.3),'po'),('b3','th'),(('b3',.05),'di')],
3:[(0.05,'ti'),(0.1,'th'),(0.35,'th'),(0.15,'wh'),('b1','po'),(('b1',.15),'po'),('b2','po'),(('b3',.1),'ti')],
4:[(0.05,'ti'),(0.1,'th'),(0.35,'th'),(('b1',-.2),'po'),(('b1',.7),'po'),('b2','th'),(('b2',.05),'di')],
5:[(0.05,'ti'),(0.1,'th'),(0.35,'th'),(0.4,'po'),('b1','po'),('b2','th'),(('b2',.2),'di')],
6:[(0.05,'ti'),(0.1,'th'),(0.35,'th'),(0.45,'po'),(1.3,'ti'),('b1','po'),(('b1',.25),'po'),(('b1',.75),'po')],
7:[(('b0',.05),'th'),(('b0',.2),'di'),('b1','th'),(('b1',.15),'di'),(('b1',.55),'th'),(('b1',.7),'di'),(0.6,'po'),('b2','th'),(('b2',.3),'th'),(('b2',.5),'po'),(('b2',1.2),'di')]}
for sc in tl.SC:
    st=sc['start'];b=sc['beats']
    for tt,k in ev[sc['i']]:
        if isinstance(tt,str): r=b[int(tt[1])]
        elif isinstance(tt,tuple): r=b[int(tt[0][1])]+tt[1]
        else: r=tt
        add(sfx,st+r,SFX[k]())
    if sc['i']<7: add(sfx,st+sc['dur']-0.38,whoosh(.42),1.1)
    # voice
    w=wave.open(f"/tmp/claude-0/kr/vo/c{sc['i']}.wav");v=np.frombuffer(w.readframes(w.getnframes()),np.int16)/32768.
    v=np.interp(np.arange(int(len(v)*SR/24000))*24000/SR,np.arange(len(v)),v)
    add(mix,st+tl.LEAD,v/np.abs(v).max()*0.9)
# music bed 120bpm
bpm=120;beat=60/bpm;bass=[55,55,65.4,49]
t=0;k=0
while t<tl.TOTAL-0.5:
    n=int(.25*SR);tt=np.arange(n)/SR;f=110*np.exp(-tt*30)+45
    add(mus,t,np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.09))
    add(mus,t+beat/2,rng.normal(0,1,int(.04*SR))*env(int(.04*SR),.008)*.35)
    bn=int(beat*SR);tb=np.arange(bn)/SR;fb=bass[(k//8)%4]
    add(mus,t+beat/2,(np.sin(2*np.pi*fb*tb)+.3*np.sin(2*np.pi*fb*2*tb))*env(bn,.18)*.5)
    t+=beat;k+=1
fade=np.clip((tl.TOTAL-np.arange(N)/SR)/1.2,0,1)
out=mix+sfx/np.abs(sfx).max()*0.42+mus/np.abs(mus).max()*0.13*fade
out=np.tanh(out*1.1)/np.tanh(1.1)*0.95
st=np.stack([out,out],1)
w=wave.open('/tmp/claude-0/kr/build/audio.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((st*32767).astype(np.int16).tobytes());w.close()
print('ok',N/SR)
