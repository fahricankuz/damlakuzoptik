#!/usr/bin/env bash
# Yarım Asır, Bölüm 6 (Zirve): medya hazırlığı ve ses miksi. Yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4), v1.mp4 (videoplayback (1).mp4)
#   ses_klasoru: anlatim6.mp3, iz6.mp3 (müziği ayrıştırılmış alıntılar: 0–6.4 = v0 439.9–446.3; 7.0–16.1 = v1 25.4–34.5),
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
vid tv       v0.mp4 437.30 9.60 "110:196:140:44" "$SOLUK" 0.2   # "365 gün, 17–18 saat" (görüntüyle senkron)
vid vitrin   v0.mp4 473.30 2.70 "110:196:137:44" "$SOLUK" 0.4   # ışıklı gözlük duvarı
vid lab      v0.mp4 619.40 2.80 "110:196:137:44" "$SOLUK" 0.4   # beyaz mağaza, atölye
vid masa     v0.mp4 476.15 2.55 "110:196:95:44"  "$SOLUK" 0.4   # Fahri Kuz masasında müşteriyle
vid raflar   v0.mp4 714.60 2.40 "110:196:40:42"  "$SOLUK" 0.4   # beyaz mağaza rafları
vid mikrofon v1.mp4 84.40  5.90 "110:196:140:46" "$SOLUK" 0.3   # mikrofonla röportaj
vid tesekkur v1.mp4 25.50  6.50 "110:196:8:46"   "$SOLUK" 0.3   # "vitrine bakarsa bir teşekkür…" (görüntüyle senkron; filigran kadraj dışında)
vid duvar2   v0.mp4 622.40 2.30 "110:196:230:44" "$SOLUK" 0.9   # beyaz mağazada çalışma masası
vid lansman  v1.mp4 640.90 3.60 "110:196:130:46" "$SOLUK" 0.3   # lansman, tanıtım ekibi
vid papagan2 v1.mp4 649.00 3.40 "110:196:125:46" "$SOLUK" 0.3   # papağan logolu kıyafetlerle tanıtım ekibi ve Fahri Kuz
vid gulumse  v0.mp4 799.00 3.40 "110:196:150:44" "$SOLUK" 0.6   # mağazada Fahri Kuz
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

D=54.5
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""; L=""; n=0
# anlatım: kaynak_baş kaynak_son kayma (videodaki yer = kaynak + kayma)
N=(0.00 7.15 9.60   7.25 18.10 10.50   18.20 24.95 20.18   25.00 27.80 20.26   27.90 29.76 21.36)
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t -v a=$a 'BEGIN{printf "%d", (t+a)*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
# Fahri Kuz: "365 gün, 17–18 saat" ve "vitrine bakarsa bir teşekkür…"
Q=(0.20 6.25 2.80   7.10 15.95 28.80)
for i in 0 1; do
  a=${Q[$((i*3))]}; b=${Q[$((i*3+1))]}; t=${Q[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.12}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[1:a]atrim=$a:$b,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.08,afade=t=out:st=$d:d=0.12,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
F+="${L}amix=inputs=$n:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[2:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=50.0:d=4.5[mu];"
SH=(9.4 14.9 17.8 28.8 38.3 48.4)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[3:a]asetpts=PTS-STARTPTS,volume=0.3,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[4:a]aloop=loop=-1:size=2e6,atrim=0:48.4,asetpts=PTS-STARTPTS,volume=0.08,afade=t=in:d=0.8,afade=t=out:st=46.8:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim6.mp3" -i "$SES/iz6.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
