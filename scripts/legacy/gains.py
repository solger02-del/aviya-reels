import numpy as np, wave, json, sys, os, subprocess
RW = os.environ["RW"]; sys.path.insert(0, RW)
from cuts import CUTS
subprocess.run(["ffmpeg","-y","-v","error","-i",f"{RW}/seg25.mp4","-vn","-ac","1","-ar","16000",f"{RW}/aud16.wav"],check=True)
w=wave.open(f"{RW}/aud16.wav"); x=np.frombuffer(w.readframes(w.getnframes()),np.int16)/32768.; sr=16000
def act(seg):
    f=seg[:len(seg)//800*800].reshape(-1,800); r=np.sqrt((f**2).mean(1)); r=r[r>10**(-45/20)]
    return 20*np.log10(np.sqrt((r**2).mean())+1e-9)
OFF = 0.21   # mono-16k -> render-level offset measured on reel 1
lv=[act(x[int(a*sr):int(b*sr)])+OFF for a,b in CUTS]
gains=[round(float(max(-4,min(9,0.7*(-15-l)))),2) for l in lv]
json.dump(gains,open(f"{RW}/speech_gains.json","w")); print([round(l,1) for l in lv]); print(gains)
