#!/usr/bin/env bash
# Yarım Asır, Bölüm 1: medya hazırlığı (renk, gren, 9:16 kırpma) ve ses miksi.
# Kullanım: ./hazirla.sh <kaynak_klasoru>
#   kaynak klasöründe: Topaz ile netleştirilmiş kapi.png muayene.png grup.png kitap.png imza.png,
#   v_bugun.mp4 v_alinti.mp4 v_90lar.mp4, anlatim.mp3 izole.mp3, sfx_deklansor.mp3 sfx_projektor.mp3
# Çıktı: assets/media/*.jpg|mp4 ve assets/audio/miks.m4a
set -euo pipefail
SRC="$1"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"

# Arşiv görünümü: sıcak siyah-beyaz, kontrast, vinyet, gren
ARSIV="format=gray,format=rgb24,colorchannelmixer=rr=1.0:gg=0.94:bb=0.82,eq=contrast=1.12:brightness=-0.02,vignette=PI/5,noise=alls=9:allf=u"
still() { # ad kaynak x y w h
  $FF -i "$SRC/$2" -vf "crop=$5:$6:$3:$4,scale=1242:2208:flags=lanczos,$ARSIV" -q:v 2 "$M/$1.jpg"
}
still kapi        kapi.png    300 0   324 576
still kapi_yakin  kapi.png    394 40  252 448
still muayene     muayene.png 133 0   324 576
still muayene_el  muayene.png 260 0   270 480
still grup        grup.png    155 0   324 576
still kitap       kitap.png   222 0   324 576
# kapanış zemini: koyu, yumuşak
$FF -i "$SRC/grup.png" -vf "crop=324:576:155:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"
# imza: yatay şerit (1080x608), hafif sıcak renk
$FF -i "$SRC/imza.png" -vf "delogo=x=984:y=80:w=84:h=82,scale=1080:608:flags=lanczos,eq=contrast=1.05:saturation=0.9,colorbalance=rs=.03:bs=-.03,vignette=PI/6,noise=alls=4:allf=u" -q:v 2 "$M/imza.jpg"

# Videolar (30 fps, 1080x1920)
# 90'lar: soluk renk
$FF -i "$SRC/v_90lar.mp4" -an -vf "crop=461:820:485:160,scale=1080:1920:flags=lanczos,fps=30,eq=saturation=0.45:contrast=1.08,colorbalance=rs=.05:gs=.01:bs=-.05,vignette=PI/5,noise=alls=8:allf=t+u,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/doksanlar.mp4"
# bugün: renk ilk 1,2 sn'de açılır (soluktan tam renge)
$FF -i "$SRC/v_bugun.mp4" -an -vf "crop=608:1080:491:0,scale=1080:1920:flags=lanczos,fps=30,eq=saturation='0.25+0.75*min(t/1.2\,1)':contrast=1.04:eval=frame,vignette=PI/6,noise=alls=3:allf=t+u,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/bugun.mp4"
# alıntı: b-roll + Fahri Kuz konuşuyor (ses ayrı miksleniyor)
$FF -i "$SRC/v_alinti.mp4" -an -vf "crop=608:1080:506:0,scale=1080:1920:flags=lanczos,fps=30,eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=3:allf=t+u,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/alinti.mp4"

# ---- Ses miksi (44 sn) ----
# anlatım cümleleri: kaynak başlangıç, bitiş, videodaki başlangıç (sn)
N=(0.00 3.46 2.40   3.88 8.20 6.80   8.54 12.70 11.90   13.00 17.25 19.20   17.70 20.24 36.40)
F=""; L=""
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}')
  ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$i];"
  L+="[n$i]"
done
# Fahri Kuz alıntısı: izole ses 73.0–81.6 → videoda 26.6
F+="[1:a]atrim=73.0:81.6,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6,afade=t=in:d=0.15,afade=t=out:st=8.2:d=0.4,adelay=26600:all=1[q];"
L+="[q]"
F+="${L}amix=inputs=6:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=44[vo];"
# müzik
F+="[2:a]atrim=0:44,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=40.5:d=3.5[mu];"
# deklanşör: arşiv kesmelerinde
SH=(3.80 6.60 9.00 11.60 13.40 18.20)
for i in "${!SH[@]}"; do
  ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}')
  F+="[3:a]asetpts=PTS-STARTPTS,volume=0.35,adelay=$ms:all=1[s$i];"
done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
# projektör: arşiv bölümü boyunca, çok kısık
F+="[4:a]aloop=loop=-1:size=2e6,atrim=0:19.0,asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:d=0.8,afade=t=out:st=17.4:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:44,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SRC/anlatim.mp3" -i "$SRC/izole.mp3" -i "$A/muzik.mp3" -i "$SRC/sfx_deklansor.mp3" -i "$SRC/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t 44 -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
