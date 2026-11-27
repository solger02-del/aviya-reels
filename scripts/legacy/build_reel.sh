#!/bin/bash
# usage: build_reel.sh <reel_dir> <out_name>
set -e
export RW=$1
cd $RW
rm -f clip_offs.json
python3 -I /home/claude/reel_scripts/render.py > /dev/null 2>&1
python3 -I /home/claude/reel_scripts/render2.py /home/claude/reel_work/silence.wav $RW/tmp_raw.mov > /dev/null
python3 - <<'PY'
import subprocess, json, glob, os
RW=os.environ["RW"]
fs=sorted(glob.glob(f"{RW}/clips/c*.mkv"))
durs=[float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",f],capture_output=True,text=True).stdout) for f in fs]
offs=[0.0]
for d in durs[:-1]: offs.append(offs[-1]+d)
json.dump({"offs":offs,"total":sum(durs)},open(f"{RW}/clip_offs.json","w"))
PY
USE_CLIP_OFFS=1 python3 -I /home/claude/reel_scripts/render.py > /dev/null 2>&1
SKIP_CLIPS=1 python3 -I /home/claude/reel_scripts/render2.py /home/claude/reel_work/silence.wav $RW/tmp_raw.mov > /dev/null
ffmpeg -hide_banner -i tmp_raw.mov -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/{/,/}/p' > ln.json
python3 - <<'PY'
import json,subprocess,os,sys
RW=os.environ["RW"]
m=json.load(open(f"{RW}/ln.json"))
af=(f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
    f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000,volume=0.6dB,alimiter=limit=0.84:level=disabled")
subprocess.run(["ffmpeg","-y","-v","error","-i",f"{RW}/tmp_raw.mov","-c:v","copy","-af",af,"-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",f"{RW}/out.mp4"],check=True)
PY
ffmpeg -hide_banner -nostats -i out.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -14 | grep -E "I:|Peak"
ffprobe -v error -show_entries format=duration,size -of compact out.mp4
