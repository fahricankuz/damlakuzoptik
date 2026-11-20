#!/usr/bin/env bash
# Yarım Asır, Bölüm 3 (Aile Dükkânı): medya hazırlığı ve ses miksi.
# Görüntüler ORİJİNAL kaynaklardan (30. Yıl filmi, v0); yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4)
#   ses_klasoru: anlatim3.mp3 sfx_deklansor.mp3 sfx_projektor.mp3
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
ARSIV="format=gray,format=rgb24,colorchannelmixer=rr=1.0:gg=0.94:bb=0.82,eq=contrast=1.1:brightness=-0.02,vignette=PI/5,noise=alls=10:allf=u"

still() { # ad saniye crop(w:h:x:y)
  $FF -ss "$2" -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=$3,scale=1242:2208:flags=lanczos,$TEMIZ,$KESKIN,$ARSIV" -q:v 2 "$M/$1.jpg"
}
still acilis      116.0 "162:288:120:0"   # Aksaray Kuz Optik: grup + vitrin (kapak görseli)
still aksaray     116.0 "162:288:30:0"    # mağaza önündeki grup
still kitap       86.0  "162:288:200:0"   # 30. yıl kitabı: metin ve genç Fahri Kuz fotoğrafı
still vitrin      116.0 "162:288:222:0"  # vitrindeki gözlük dizileri
still goz         104.0 "150:267:100:10"  # muayene: eller ve cihaz
still kapi        70.0  "162:288:180:0"   # mağaza kapısında genç Fahri Kuz
still kapi_yakin  70.0  "130:231:195:10"
# Sirkeci: eski İstanbul hava görüntüsü (filigransız sol kenar)
$FF -ss 30.0 -t 3.6 -i "$FK/v0.mp4" -an -vf "crop=128:228:0:30,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$ARSIV,tpad=stop_mode=clone:stop_duration=0.4,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/sirkeci.mp4"
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

# ---- Ses miksi ----
D=36.5
F=""; L=""
# anlatım cümleleri: kaynak başlangıç, bitiş, videodaki başlangıç
N=(0.00 1.45 3.00   1.70 6.45 5.40   6.80 10.55 10.60   10.80 11.48 15.20   11.74 19.40 17.00   19.70 21.80 25.40   22.14 24.16 30.00)
for i in 0 1 2 3 4 5 6; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$i];"; L+="[n$i]"
done
F+="${L}amix=inputs=7:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
# müzik: "Yanıldılar" anında kısa bir sessizlik (14.6–16.6 arası müzik kısılır)
F+="[1:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,volume='if(between(t,14.7,16.7),0.25,1)':eval=frame,afade=t=in:d=1.0,afade=t=out:st=33.0:d=3.5[mu];"
SH=(2.80 5.40 10.40 16.80 20.00 22.40)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[2:a]asetpts=PTS-STARTPTS,volume=0.35,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[3:a]aloop=loop=-1:size=2e6,atrim=0:29.0,asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:d=0.8,afade=t=out:st=27.4:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim3.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
