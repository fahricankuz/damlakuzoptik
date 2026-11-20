#!/usr/bin/env bash
# Yarım Asır, Bölüm 5 (Kendi adı): medya hazırlığı ve ses miksi. Yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4), v1.mp4 (videoplayback (1).mp4)
#   ses_klasoru: anlatim5.mp3, iz5.mp3 (müziği ayrıştırılmış alıntılar: 0–12.4 = v0 742.6–755.0; 13.0–21.4 = v0 575.9–584.3),
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
vid duvar    v1.mp4 213.60 2.50 "110:196:55:46" "$SOLUK" 0.6   # Fahri Kuz gözlük duvarında
vid isaret   v1.mp4 221.00 2.10 "110:196:150:46" "$SOLUK" 0.5   # gözlük duvarını gösteriyor
bant tabela  v1.mp4 210.95 2.30 0.4   # "Fahri Kuz Optik" tabelası ve aydınlık vitrin (tam kare)
vid atrium   v1.mp4 203.00 3.20 "110:196:125:46" "$SOLUK" 0.4   # AVM içindeki mağaza kapısında
vid yuruyus  v1.mp4 206.50 2.00 "110:196:130:46" "$SOLUK" 0.4   # AVM'de yürüyüş
vid tezgah   v1.mp4 216.50 3.90 "110:196:175:46" "$SOLUK" 0.5   # tezgâhta müşteriyle
bant acilis  v1.mp4 631.20 2.60 0.4   # mağaza açılışı, kalabalık (tam kare)
vid papagan  v0.mp4 711.20 2.40 "110:196:186:42" "$SOLUK" 0.4   # rafın üstünde çerçeveli papağan
vid cicek    v0.mp4 576.30 3.95 "110:196:172:44" "$SOLUK" 0.3   # "Kırda dahi bir çiçek…" (görüntüyle senkron)
vid ofis     v1.mp4 229.00 4.00 "110:196:70:46" "$SOLUK" 0.4   # makam odasında
vid deneme   v1.mp4 662.62 3.80 "110:196:137:46" "$SOLUK" 0.5   # gözlük deneyen müşteriler
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

D=44.5
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""; L=""; n=0
# anlatım: kaynak_baş kaynak_son videodaki_yer
N=(0.00 3.55 2.60   3.60 5.30 16.60   5.40 8.50 18.90   8.60 12.45 33.40   12.55 14.56 38.60)
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
# Fahri Kuz: Atrium/Akmerkez (üç parça, tekrar eden "Atrium'da" çıkarıldı) ve "Kırda dahi bir çiçek…"
Q=(0.30 2.45 6.60   3.20 5.70 8.95   7.85 12.05 11.80   13.40 21.30 25.00)
for i in 0 1 2 3; do
  a=${Q[$((i*3))]}; b=${Q[$((i*3+1))]}; t=${Q[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.12}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[1:a]atrim=$a:$b,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.08,afade=t=out:st=$d:d=0.12,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
F+="${L}amix=inputs=$n:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[2:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=40.5:d=4.0[mu];"
SH=(7.2 16.3 18.6 20.55 37.4)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[3:a]asetpts=PTS-STARTPTS,volume=0.3,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[4:a]aloop=loop=-1:size=2e6,atrim=0:37.4,asetpts=PTS-STARTPTS,volume=0.08,afade=t=in:d=0.8,afade=t=out:st=35.8:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim5.mp3" -i "$SES/iz5.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
