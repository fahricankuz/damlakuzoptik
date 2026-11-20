#!/usr/bin/env bash
# Bölüm 10 (Kuz İstanbul açılış duyurusu): ses miksi.
# ses/muzik.mp3 (ElevenLabs, 117 BPM; yüksek bölüm 16,23 sn'de başlar), whoosh.mp3 (tepe 0,4 sn), tik.mp3, basari.mp3
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/audio
D=30.0
# geçiş sesleri: görüntüdeki an (sn); dosyanın tepe noktası 0,4 sn olduğu için 0,4 erken başlatılır
WH=(4.15 10.2 14.2 19.25 22.3 25.85)
TK=(16.15 21.27)
F="[0:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=1.0,afade=t=out:st=28.6:d=1.4[mu];"
L="[mu]"; n=1
for i in "${!WH[@]}"; do ms=$(awk -v t=${WH[$i]} 'BEGIN{printf "%d", (t-0.4)*1000}'); F+="[1:a]volume=0.32,adelay=$ms:all=1[w$i];"; L+="[w$i]"; n=$((n+1)); done
for i in "${!TK[@]}"; do ms=$(awk -v t=${TK[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[2:a]volume=0.55,adelay=$ms:all=1[t$i];"; L+="[t$i]"; n=$((n+1)); done
F+="[3:a]volume=0.4,adelay=12300:all=1[b0];"; L+="[b0]"; n=$((n+1))
F+="${L}amix=inputs=$n:normalize=0:duration=first,atrim=0:$D,loudnorm=I=-14:TP=-1.0:LRA=9,aresample=48000[a]"
ffmpeg -v error -y -i ses/muzik.mp3 -i ses/whoosh.mp3 -i ses/tik.mp3 -i ses/basari.mp3 -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k assets/audio/miks.m4a
echo hazir
