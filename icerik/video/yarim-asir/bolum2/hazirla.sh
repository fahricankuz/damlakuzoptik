#!/usr/bin/env bash
# Yarım Asır, Bölüm 2 (Usta Eli): medya hazırlığı ve ses miksi.
# Görüntüler ORİJİNAL kaynaklardan; yapay zekâ netleştirmesi yok. Klasik işlemler: kare ortalaması, lanczos, hafif keskinlik, renk, gren.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (videoplayback.mp4), v2.mp4 (videoplayback (2).mp4)
#   ses_klasoru: anlatim2.mp3 q1_izole.mp3 (v0 315.3–323.9, müziği ayrıştırılmış) izole.mp3 (v2 tamamı, müziği ayrıştırılmış)
#                sfx_deklansor.mp3 sfx_projektor.mp3
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
ARSIV="format=gray,format=rgb24,colorchannelmixer=rr=1.0:gg=0.94:bb=0.82,eq=contrast=1.1:brightness=-0.02,vignette=PI/5,noise=alls=10:allf=u"
SOLUK="eq=saturation=0.45:contrast=1.08,colorbalance=rs=.05:gs=.01:bs=-.05,vignette=PI/5,noise=alls=9:allf=t+u"
RENK="eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u"

still() { # ad kaynak saniye crop(w:h:x:y) görünüm
  $FF -ss "$3" -i "$FK/$2" -frames:v 1 -vf "tmix=frames=5,crop=$4,scale=1242:2208:flags=lanczos,$TEMIZ,$KESKIN,$5" -q:v 2 "$M/$1.jpg"
}
vid() { # ad kaynak baslangic sure crop görünüm bekletme [ön_filtre]
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -vf "${8:-null},crop=$5,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$6,tpad=stop_mode=clone:stop_duration=$7,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/$1.mp4"
}

still acilis    v0.mp4 113.0 "108:192:106:20" "$ARSIV"            # mağaza önü fotoğrafında genç Fahri Kuz
vid   sirkeci   v0.mp4 30.0  4.8 "128:228:256:20" "$ARSIV" 0.4    # eski İstanbul (filigransız sağ kenar)
vid   roportaj  v0.mp4 316.0 7.8 "116:206:100:40"  "$SOLUK" 0.4     # 90'lar TV röportajı (logo ve alt bant dışarıda)
vid   olcum     v0.mp4 605.0 3.9 "115:205:175:40" "$SOLUK" 0.4     # 90'lar göz ölçümü (604.08 ve 611.52 kesmeleri arası)
still goz       v0.mp4 99.9  "110:196:50:30"  "$ARSIV"             # sepya muayene, yakın
vid   detay1    v2.mp4 23.95 1.45 "202:360:144:0" "$RENK" 0.6      # büst ve gözlük (kaynak kesmeleri arası)
vid   detay2    v2.mp4 25.50 1.42 "202:360:144:0" "$RENK" 0.6
vid   detay3    v2.mp4 27.02 1.42 "202:360:140:0" "$RENK" 0.6
vid   detay4    v2.mp4 28.54 1.42 "202:360:140:0" "$RENK" 1.2
vid   bugun     v2.mp4 60.3  5.6 "202:360:140:0" "eq=saturation='0.3+0.7*min(t/1.0\,1)':contrast=1.04:eval=frame,vignette=PI/6,noise=alls=4:allf=t+u" 0.6
vid   raflar    v2.mp4 15.15 2.0 "202:360:60:0"  "$RENK" 0.6       # mağaza duvarı (15.08–17.24 arası)
vid   raf_yakin v2.mp4 19.45 2.0 "202:360:100:0" "$RENK" 0.6       # raflar yakın (19.40–21.56 arası)
vid   gozluk    v2.mp4 41.42 2.0 "202:360:140:0" "$RENK" 0.6       # gözlük yakın plan (41.36 sonrası)
vid   fk_simdi  v2.mp4 10.2  4.7 "202:360:140:0" "$RENK" 0.8       # Fahri Kuz bugün (yazı ve nokta kadraj dışında)
$FF -ss 113.0 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"

# ---- Ses miksi (52 sn) ----
D=52
VOICE="highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6"
F=""
# anlatım cümleleri: kaynak başlangıç, bitiş, videodaki başlangıç
N=(0.00 3.45 3.00   3.70 9.45 15.10   9.67 13.45 29.20   13.68 24.75 33.40   24.99 26.88 46.00)
L=""
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}'); ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$i];"; L+="[n$i]"
done
# Fahri Kuz 1 (90'lar röportajı): dosya 315.3'te başlar → videoda 6.6 (görüntüyle senkron)
F+="[1:a]atrim=0.2:8.2,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.25,afade=t=out:st=7.5:d=0.5,adelay=6800:all=1[q1];"; L+="[q1]"
# Fahri Kuz 2 (tanıtım filmi): v2 31.1–37.75 → videoda 22.4
F+="[2:a]atrim=31.1:37.75,asetpts=PTS-STARTPTS,$VOICE,afade=t=in:d=0.25,afade=t=out:st=6.15:d=0.5,adelay=22400:all=1[q2];"; L+="[q2]"
F+="${L}amix=inputs=7:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=$D[vo];"
F+="[3:a]atempo=0.865,atrim=0:$D,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=48.0:d=4.0[mu];"
SH=(2.80 7.30 14.80 18.50)
for i in "${!SH[@]}"; do ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}'); F+="[4:a]asetpts=PTS-STARTPTS,volume=0.35,adelay=$ms:all=1[s$i];"; done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[5:a]aloop=loop=-1:size=2e6,atrim=0:22.4,asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:d=0.8,afade=t=out:st=20.8:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim2.mp3" -i "$SES/q1_izole.mp3" -i "$SES/izole.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
