#!/usr/bin/env bash
# Yarım Asır, Bölüm 7 (Devir): medya hazırlığı ve ses miksi. Yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4), v1.mp4 (videoplayback (1).mp4), v2.mp4 (videoplayback (2).mp4)
#   ses_klasoru: anlatim7.mp3 (yalnızca anlatıcı; bu bölümde Fahri Kuz alıntısı yok),
#                sfx_deklansor.mp3, sfx_projektor.mp3
# Not: v1 karelerinin bir kısmında yazılım filigranı var; seçilen aralıklar filigransızdır. Üstteki kanal bandı kadraj dışında.
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
SOLUK="eq=saturation=0.55:contrast=1.08,colorbalance=rs=.05:gs=.01:bs=-.05,vignette=PI/5,noise=alls=9:allf=t+u"
vid() { # ad kaynak baslangic sure crop görünüm bekletme
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -vf "crop=$5,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$6,tpad=stop_mode=clone:stop_duration=$7,format=yuv420p" -c:v libx264 -crf 18 -preset medium -g 30 "$M/$1.mp4"
}
bant() { # ad kaynak baslangic sure bekletme: 4:3 kare ortada, arkada bulanık büyütülmüş hali
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -filter_complex "[0:v]crop=376:200:4:46,fps=30,$TEMIZ,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=28,eq=brightness=-0.18[bg];[b]scale=1080:574:flags=lanczos,$KESKIN[fg];[bg][fg]overlay=0:420,$SOLUK,tpad=stop_mode=clone:stop_duration=$5,format=yuv420p" -c:v libx264 -crf 18 -preset medium -g 30 "$M/$1.mp4"
}
bant lazer   v1.mp4 840.00 6.40 0.6   # 2000, 30. yıl kutlaması: lazerle "30. YIL" (tam kare)
bant defile  v1.mp4 668.30 4.50 0.8   # 30. yıl defilesi, arka planda Fahri Kuz yazısı (tam kare)
vid  bugun   v2.mp4 83.70  2.90 "202:360:120:0" "eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u" 1.7   # bugün Fahri Kuz (Bölüm 8 ile tekrar etmesin diye 83,7 sn; etiket kadraj dışında)
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

D=46.4
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""; L=""; n=0
# anlatım: kaynak_baş kaynak_son kayma (videodaki yer = kaynak + kayma)
N=(0.00 2.95 2.80   3.05 6.35 2.81   6.45 8.15 2.71   8.25 10.00 2.79   10.05 14.85 6.39   14.90 19.40 6.57   19.45 21.55 6.72   21.60 23.25 6.76   23.30 25.04 17.93)
for i in 0 1 2 3 4 5 6 7 8; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t -v a=$a 'BEGIN{printf "%d", (t+a)*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
F+="${L}amix=inputs=$n:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[1:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=42.4:d=4.0[mu];"
SH=(5.4 11.0 16.3 21.3 31.2 36.2 40.4)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[2:a]asetpts=PTS-STARTPTS,volume=0.3,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[3:a]aloop=loop=-1:size=2e6,atrim=0:40.4,asetpts=PTS-STARTPTS,volume=0.08,afade=t=in:d=0.8,afade=t=out:st=38.8:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim7.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
