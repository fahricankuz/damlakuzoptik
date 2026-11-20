#!/usr/bin/env bash
# Yarım Asır, Bölüm 9 (Final, DEMO): Kuz İstanbul. Hafıza montajı ve ses miksi.
# Kullanım: ./hazirla.sh <ses_ve_marka_klasoru>
#   klasör: muzikA.mp3 muzikB.mp3 anlatim9.mp3 gecici_ses.mp3 damla.mp3 marka/brosur1.png marka/brosur2.png
# Montaj, önceki bölümlerin altyazısız medya dosyalarından kurulur (../bolumX/assets/media).
set -euo pipefail
E="$1"
cd "$(dirname "$0")"
M=assets/media; A=assets/audio; T=$(mktemp -d)
mkdir -p "$M" "$A"
FF="ffmpeg -v error -y"
SEPYA="format=gray,format=rgb24,colorchannelmixer=rr=1:gg=.93:bb=.80,eq=contrast=1.06:brightness=-0.02"
DOGAL="eq=contrast=1.05:saturation=0.9"
GREN="noise=alls=6:allf=t+u,vignette=PI/5"

# ad | kaynak | başlangıç | görünüm   (süreler aşağıda hesaplanır, hızlanan kurgu)
LISTE=(
  "../bolum3/assets/media/aksaray.jpg|0|$SEPYA"
  "../bolum2/assets/media/sirkeci.mp4|1.0|$SEPYA"
  "../bolum1/assets/media/muayene.jpg|0|$SEPYA"
  "$E/marka/brosur1.png|0|$DOGAL"
  "../bolum1/assets/media/kapi.jpg|0|$SEPYA"
  "$E/marka/brosur2.png|0|$DOGAL"
  "../bolum5/assets/media/tabela.mp4|0.2|$DOGAL"
  "../bolum5/assets/media/duvar.mp4|0.5|$DOGAL"
  "../bolum5/assets/media/papagan.mp4|0.6|$DOGAL"
  "../bolum6/assets/media/lansman.mp4|0.6|$DOGAL"
  "../bolum6/assets/media/tv.mp4|3.2|$DOGAL"
  "../bolum7/assets/media/lazer.mp4|3.3|$DOGAL"
  "../bolum7/assets/media/defile.mp4|1.0|$DOGAL"
)
: > "$T/liste.txt"
i=0
for satir in "${LISTE[@]}"; do
  IFS='|' read -r src ss gor <<< "$satir"
  d=$(awk -v i=$i 'BEGIN{printf "%.3f", (i==0?1.95:1.75) - 0.07*i}')
  out="$T/p$(printf %02d $i).mp4"
  case "$src" in
    *.jpg|*.png)
      $FF -loop 1 -t "$d" -i "$src" -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=1200:2133,zoompan=z='1+0.0016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,$gor,$GREN,format=yuv420p" -t "$d" -c:v libx264 -crf 17 -preset medium -r 30 "$out" ;;
    *)
      $FF -ss "$ss" -t "$d" -i "$src" -an -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,$gor,$GREN,tpad=stop_mode=clone:stop_duration=1,format=yuv420p" -t "$d" -c:v libx264 -crf 17 -preset medium -r 30 "$out" ;;
  esac
  echo "file '$out'" >> "$T/liste.txt"
  i=$((i+1))
done
for p in "$T"/p*.mp4; do ffprobe -v error -show_entries format=duration -of csv=p=0 "$p"; done > "$M/montaj_parcalar.txt"
$FF -f concat -safe 0 -i "$T/liste.txt" -c:v libx264 -crf 17 -preset medium -r 30 -g 30 "$M/montaj.mp4"
# bugünden Fahri Kuz (marka dünyası arka planı için yavaş, renkli)
$FF -ss 0.2 -t 5.4 -i ../bolum8/assets/media/bugun.mp4 -an -vf "fps=30,eq=contrast=1.04:saturation=0.85,format=yuv420p" -c:v libx264 -crf 18 -preset medium -g 30 "$M/fk_bugun.mp4"

D=84.8
F=""
F+="[0:a]afade=t=in:d=0.8,afade=t=out:st=22.4:d=1.3,volume=0.85,apad=whole_dur=$D[ma];"
F+="[1:a]adelay=31000:all=1,volume=0.95,afade=t=out:st=81.6:d=3.2,apad=whole_dur=$D[mb];"
F+="[2:a]atrim=0:2.72,asetpts=PTS-STARTPTS,afade=t=out:st=2.62:d=0.1,adelay=1200:all=1,apad=whole_dur=$D[v1];"
F+="[2:a]atrim=2.95:5.76,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,adelay=67800:all=1,apad=whole_dur=$D[v2];"
F+="[3:a]atrim=0:4.05,asetpts=PTS-STARTPTS,adelay=73300:all=1,apad=whole_dur=$D[v3];"
F+="[4:a]volume=1.2,adelay=32950:all=1,apad=whole_dur=$D[dm];"
F+="[v1][v2][v3]amix=inputs=3:normalize=0,volume=1.5[vo];[vo]asplit=2[vo1][vo2];"
F+="[mb][vo2]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=500[mbd];"
F+="[ma][mbd][dm][vo1]amix=inputs=4:normalize=0:duration=longest,atrim=0:$D,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]"
$FF -i "$E/muzikA.mp3" -i "$E/muzikB.mp3" -i "$E/anlatim9.mp3" -i "$E/gecici_ses.mp3" -i "$E/damla.mp3" \
  -filter_complex "$F" -map "[a]" -t $D -c:a aac -b:a 192k "$A/miks.m4a"
echo "hazir"
