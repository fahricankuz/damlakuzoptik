#!/usr/bin/env bash
# Yarım Asır, Bölüm 8 (Bugün): medya hazırlığı ve ses miksi. Yapay zekâ netleştirmesi yok.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4), v2.mp4 (videoplayback (2).mp4)
#   ses_klasoru: anlatim8.mp3, s1.mp3 (ilk cümlenin yeni hali), izole.mp3 (v2'nin müziği ayrıştırılmış sesi), sfx_deklansor.mp3, sfx_projektor.mp3
# Online mağaza ekranları (assets/media/asistan1-3.jpg) damlakuzoptik.com'dan, kampanya bandı gizlenerek alındı.
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
RENK="eq=contrast=1.04:saturation=0.98,vignette=PI/6,noise=alls=4:allf=t+u"
vid() { # ad kaynak baslangic sure crop yavaslatma bekletme
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -vf "crop=$5,setpts=$6*PTS,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$RENK,tpad=stop_mode=clone:stop_duration=$7,format=yuv420p" -c:v libx264 -crf 18 -preset medium -g 30 "$M/$1.mp4"
}
bant() { # ad kaynak baslangic sure yavaslatma bekletme: 16:9 kare ortada, arkada bulanık hali
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -filter_complex "[0:v]crop=600:226:10:45,setpts=$5*PTS,fps=30,$TEMIZ,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30,eq=brightness=-0.2[bg];[b]scale=1080:406:flags=lanczos,$KESKIN[fg];[bg][fg]overlay=0:470,$RENK,tpad=stop_mode=clone:stop_duration=$6,format=yuv420p" -c:v libx264 -crf 18 -preset medium -g 30 "$M/$1.mp4"
}
vid  kutular  v2.mp4 0.05  1.50 "150:266:60:46"   2.0 0.3    # kutular üzerinde gözlükler (yavaş; başlık için koyulaştırılır)
bant magaza   v2.mp4 4.10  2.10 1.9 3.6                     # Ataköy Atrium AVM mağazası, tabela (yavaş)
vid  bugun    v2.mp4 66.00 5.40 "202:360:150:0"  1.0 0.4    # Fahri Kuz mağazada
vid  el       v2.mp4 92.05 1.10 "202:360:219:0"  2.0 0.2    # altın el üzerinde gözlükler (yavaş)
vid  figur    v2.mp4 91.05 0.90 "202:360:60:0"   2.0 0.3    # figür ve gözlükler (yavaş)
vid  beyaz    v2.mp4 45.60 6.00 "202:360:100:0"  1.0 0.4    # "Beyazı daha beyaz…" (görüntüyle senkron)
vid  simdi    v2.mp4 82.00 1.40 "202:360:120:0"  1.3 0.2    # bugün Fahri Kuz (yakın)
$FF -ss 113.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=108:192:106:20,scale=1080:1920:flags=lanczos,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=contrast=1.05,vignette=PI/4,noise=alls=7:allf=u" -q:v 2 "$M/genc.jpg"
$FF -ss 116.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

D=52.0
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""; L=""; n=0
# anlatım: kaynak_baş kaynak_son kayma (videodaki yer = kaynak + kayma)
N=(4.10 10.30 6.42   10.35 14.60 6.59   14.65 17.70 13.57   17.75 20.70 20.76   20.75 23.55 21.39   23.60 25.20 22.64)
for i in 0 1 2 3 4 5; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t -v a=$a 'BEGIN{printf "%d", (t+a)*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
# yeni ilk cümle: "Durmadı." / "Kuz Optik'e bir damla ekledi ve yoluna kızının adıyla devam etti:" / "Damla Kuz Optik."
P=(0.00 0.60 1.50   0.84 4.45 1.46   4.98 6.25 1.17)
for i in 0 1 2; do
  a=${P[$((i*3))]}; b=${P[$((i*3+1))]}; t=${P[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t -v a=$a 'BEGIN{printf "%d", (t+a)*1000}')
  F+="[4:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
# Fahri Kuz: "On sene aradan sonra tekrar Ataköy AVM'deyiz." ve "Beyazı daha beyaz…"
Q=(19.72 22.62 7.62   45.62 51.98 21.52)
for i in 0 1; do
  a=${Q[$((i*3))]}; b=${Q[$((i*3+1))]}; t=${Q[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.12}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[1:a]atrim=$a:$b,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.08,afade=t=out:st=$d:d=0.12,adelay=$ms:all=1[n$n];"; L+="[n$n]"; n=$((n+1))
done
F+="${L}amix=inputs=$n:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[2:a]atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=48.0:d=4.0[mu];"
SH=(3.0 10.4 16.8 21.5 28.1 33.6 38.4 45.4)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[3:a]asetpts=PTS-STARTPTS,volume=0.25,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh]amix=inputs=3:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-15:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim8.mp3" -i "$SES/izole.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/s1.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
