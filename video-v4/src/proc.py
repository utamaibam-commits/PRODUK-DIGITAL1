import numpy as np, wave, json, subprocess
def rd(f):
    w=wave.open(f);a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32);return a,w.getframerate()
out={}
for s in range(1,8):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'vo/s{s}.wav','-filter:a','atempo=1.10','-ar','24000','-ac','1',f'vo/t{s}.wav'])
    a,sr=rd(f'vo/t{s}.wav')
    win=int(sr*0.01);n=len(a)//win
    rms=np.array([np.sqrt(np.mean(a[i*win:(i+1)*win]**2)) for i in range(n)])
    loud=rms>=200
    idx=np.where(loud)[0];st,en=idx[0],idx[-1]+1
    # find silences
    segs=[];i=st
    while i<en:
        if not loud[i]:
            j=i
            while j<en and not loud[j]: j+=1
            segs.append((i,j));i=j
        else:i+=1
    pieces=[];beats=[0.0];cur=st;outlen=0
    for (i,j) in segs:
        L=(j-i)*0.01
        if L>=0.2:
            pieces.append(a[cur*win:i*win]);outlen+=(i-cur)*win
            gap=int(0.16*sr);pieces.append(np.zeros(gap));outlen+=gap
            beats.append(outlen/sr);cur=j
    pieces.append(a[cur*win:en*win])
    y=np.concatenate(pieces).astype(np.int16)
    w=wave.open(f'vo/c{s}.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(y.tobytes());w.close()
    out[s]={'dur':len(y)/sr,'beats':beats}
    print(s,round(len(y)/sr,2),[round(b,2) for b in beats])
json.dump(out,open('vo/beats.json','w'))
