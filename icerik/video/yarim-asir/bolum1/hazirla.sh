#!/usr/bin/env bash
# Yarım Asır, Bölüm 1: medya hazırlığı ve ses miksi.
# Görüntüler ORİJİNAL kaynaklardan alınır; yapay zekâ netleştirmesi kullanılmaz (kullanıcı kararı, 20 Kasım 2026).
# Yalnızca yüzü/yapıyı değiştirmeyen klasik işlemler: kare ortalamasıyla gürültü azaltma, lanczos büyütme,
# hafif keskinlik, renk ve gren.
# Kullanım: ./hazirla.sh <fk_klasoru> <ses_klasoru>
#   fk_klasoru: v0.mp4 (Drive > Fahri Kuz > videoplayback.mp4), v2.mp4 (videoplayback (2).mp4)
#   ses_klasoru: anlatim.mp3 izole.mp3 sfx_deklansor.mp3 sfx_projektor.mp3
set -euo pipefail
FK="$1"; SES="$2"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"

TEMIZ="hqdn3d=1.5:1.5:2:2"
KESKIN="unsharp=5:5:0.35:5:5:0"
ARSIV="format=gray,format=rgb24,colorchannelmixer=rr=1.0:gg=0.94:bb=0.82,eq=contrast=1.1:brightness=-0.02,vignette=PI/5,noise=alls=10:allf=u"

# Arşiv kareleri: v0'dan, 5 kare ortalaması (gürültü azaltma), 9:16 kırpma
still() { # ad saniye x y w h
  $FF -ss "$2" -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=$5:$6:$3:$4,scale=1242:2208:flags=lanczos,$TEMIZ,$KESKIN,$ARSIV" -q:v 2 "$M/$1.jpg"
}
still kapi        67.9  150 0   162 288
still kapi_yakin  67.9  197 20  126 224
still muayene     99.9  66  0   162 288
still muayene_el  99.9  130 0   135 240
still grup        114.9 77  0   162 288
$FF -ss 114.9 -i "$FK/v0.mp4" -frames:v 1 -vf "tmix=frames=5,crop=162:288:77:0,scale=1242:2208,format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.94:bb=.82,eq=brightness=-0.22:contrast=1.05,gblur=sigma=6,vignette=PI/3.5,noise=alls=6:allf=u" -q:v 2 "$M/kapanis_zemin.jpg"
# İmza: v2 52.3 sn, yatay şerit; arayüzden kalan beyaz nokta temizlenir
$FF -ss 52.3 -i "$FK/v2.mp4" -frames:v 1 -vf "tmix=frames=3,delogo=x=492:y=40:w=42:h=41,scale=1080:608:flags=lanczos,$TEMIZ,$KESKIN,eq=contrast=1.05:saturation=0.9,colorbalance=rs=.03:bs=-.03,vignette=PI/6,noise=alls=4:allf=u" -q:v 2 "$M/imza.jpg"

# Videolar (30 fps, 1080x1920)
vid() { # ad kaynak baslangic sure crop ek_filtre bekletme(sn)
  $FF -ss "$3" -t "$4" -i "$FK/$2" -an -vf "crop=$5,scale=1080:1920:flags=lanczos,fps=30,$TEMIZ,$KESKIN,$6,tpad=stop_mode=clone:stop_duration=$7,format=yuv420p" -c:v libx264 -crf 18 -preset medium "$M/$1.mp4"
}
# 90'lar: soluk renk (kesme yok: 612.2–617.0)
vid doksanlar v0.mp4 612.2 4.8 "115:205:121:40" "eq=saturation=0.45:contrast=1.08,colorbalance=rs=.05:gs=.01:bs=-.05,vignette=PI/5,noise=alls=9:allf=t+u" 0.6
# bugün: kaynakta 32.04'te kesme var, sonrasından başlar; renk ilk 1,2 sn'de açılır
vid bugun v2.mp4 32.1 4.4 "203:360:164:0" "eq=saturation='0.25+0.75*min(t/1.2\,1)':contrast=1.04:eval=frame,vignette=PI/6,noise=alls=4:allf=t+u" 0.6
# alıntı: kaynakta 73.48, 75.48, 77.48'de kesmeler var; üç parçaya bölünür, aralarda yumuşak geçiş yapılır
vid alinti_a v2.mp4 73.50 1.98 "203:360:169:0" "eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u" 0.6
vid alinti_b v2.mp4 75.50 1.98 "203:360:169:0" "eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u" 0.6
vid alinti_c v2.mp4 77.50 4.20 "203:360:169:0" "eq=contrast=1.04:saturation=0.95,vignette=PI/6,noise=alls=4:allf=t+u" 1.2

# ---- Ses miksi (44 sn) ----
N=(0.00 3.46 2.40   3.88 8.20 6.80   8.54 12.70 11.90   13.00 17.25 19.20   17.70 20.24 36.40)
F=""; L=""
for i in 0 1 2 3 4; do
  a=${N[$((i*3))]}; b=${N[$((i*3+1))]}; t=${N[$((i*3+2))]}
  d=$(awk -v a=$a -v b=$b 'BEGIN{printf "%.2f", b-a-0.06}')
  ms=$(awk -v t=$t 'BEGIN{printf "%d", t*1000}')
  F+="[0:a]atrim=$a:$b,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=$d:d=0.06,adelay=$ms:all=1[n$i];"
  L+="[n$i]"
done
# Fahri Kuz alıntısı: izole ses 73.0–81.7 → videoda 26.6; yumuşak giriş ve çıkış
F+="[1:a]atrim=73.0:81.7,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=9500,afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6,afade=t=in:d=0.3,afade=t=out:st=8.1:d=0.6,adelay=26600:all=1[q];"
L+="[q]"
F+="${L}amix=inputs=6:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur=44[vo];"
F+="[2:a]atrim=0:44,asetpts=PTS-STARTPTS,volume=0.6,afade=t=in:d=1.0,afade=t=out:st=40.5:d=3.5[mu];"
SH=(3.80 6.60 9.00 11.60 13.40)
for i in "${!SH[@]}"; do
  ms=$(awk -v t=${SH[$i]} 'BEGIN{printf "%d", t*1000}')
  F+="[3:a]asetpts=PTS-STARTPTS,volume=0.35,adelay=$ms:all=1[s$i];"
done
SL=$(for i in "${!SH[@]}"; do printf "[s$i]"; done)
F+="${SL}amix=inputs=${#SH[@]}:normalize=0[sh];"
F+="[4:a]aloop=loop=-1:size=2e6,atrim=0:19.0,asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:d=0.8,afade=t=out:st=17.4:d=1.6[pr];"
F+="[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud];"
F+="[vo1][mud][sh][pr]amix=inputs=4:normalize=0:duration=longest,atrim=0:44,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$SES/anlatim.mp3" -i "$SES/izole.mp3" -i "$A/muzik.mp3" -i "$SES/sfx_deklansor.mp3" -i "$SES/sfx_projektor.mp3" \
  -filter_complex "$F" -map "[a]" -t 44 -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
