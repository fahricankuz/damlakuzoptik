#!/usr/bin/env bash
# Yarım Asır, Bölüm 4 (Fabrika): medya hazırlığı ve ses miksi. Yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4, v2.mp4   ses_klasoru: anlatim4.mp3 q1_izole.mp3 (v0 351.2–356.4) izole.mp3 (v2) sfx_deklansor.mp3 sfx_projektor.mp3
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
SOLUK="eq=saturation=0.45:contrast=1.08,colorbalance=rs=.05:gs=.01:bs=-.05,vignette=PI/5,noise=alls=9:allf=t+u"
RENK="eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u"
vid() { # ad kaynak baslangic sure crop görünüm bekletme
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -vf "crop=$5,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$6,tpad=stop_mode=clone:stop_duration=$7,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/$1.mp4"
}
vid roportaj v0.mp4 353.50 2.0  "116:206:100:38"  "$SOLUK" 0.5   # 90'lar STV: "Türkiye'de yapılan var"
vid ozel     v2.mp4 6.42  2.70 "136:242:298:54"  "$RENK" 0.3   # "kişiye özel" yuvarlak degrade cam (6.28–9.36 arası; yazı ve nokta kadraj dışında)
vid mor      v2.mp4 71.55 1.88 "202:360:150:0"  "$RENK" 0.3   # mor kutu üzerinde çerçevesiz gözlük (71.48–73.48 arası)
vid raf      v2.mp4 54.48 1.26 "202:360:260:0"  "$RENK" 0.5   # rafta pembe güneş gözlüğü (54.44–55.76 arası)
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

D=39.5
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""; L=""
N=(0.00 5.30 2.40   5.50 12.10 11.20   12.25 17.55 18.20   17.70 20.40 29.20   20.58 22.32 32.80)
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$i];"; L+="[n$i]"
done
# Fahri Kuz 1 (v0 351.2 → videoda 6.8; görüntüyle senkron)
F+="[1:a]atrim=1.15:3.5,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.15,afade=t=out:st=1.95:d=0.4,adelay=7950:all=1[q1];"; L+="[q1]"
# Fahri Kuz 2 (v2 26.35–31.0 → videoda 23.85)
F+="[2:a]atrim=26.35:31.0,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.2,afade=t=out:st=4.2:d=0.45,adelay=23850:all=1[q2];"; L+="[q2]"
F+="${L}amix=inputs=7:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[3:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=36.0:d=3.5[mu];"
SH=(9.05 23.70 26.30 28.05)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[4:a]asetpts=PTS-STARTPTS,volume=0.3,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[5:a]aloop=loop=-1:size=2e6,atrim=0:23.6,asetpts=PTS-STARTPTS,volume=0.08,afade=t=in:d=0.8,afade=t=out:st=22.0:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim4.mp3" -i "$SES/q1_izole.mp3" -i "$SES/izole.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
