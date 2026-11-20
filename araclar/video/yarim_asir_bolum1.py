#!/usr/bin/env python3
"""Yarım Asır, Bölüm 1: 9:16 Reels kurgusu (ffmpeg).

Kullanım:
    python3 yarim_asir_bolum1.py <kaynak_klasoru> <calisma_klasoru> <font_klasoru> <cikti.mp4>

kaynak_klasoru içinde beklenen dosyalar:
    v0.mp4   Drive > Fahri Kuz > videoplayback.mp4 (30. Yıl + Basında)
    v2.mp4   Drive > Fahri Kuz > videoplayback (2).mp4 (tanıtım filmi)
calisma_klasoru içinde beklenen dosyalar:
    anlatim.mp3  ElevenLabs anlatım (Cem), 5 cümle
    izole.mp3    tanıtım filminin müziksiz (voice isolator) sesi
    muzik.mp3    ElevenLabs müzik
"""
import subprocess
import sys
from pathlib import Path

SRC, WORK, FONTS, OUT = (Path(a) for a in sys.argv[1:5])
FPS = 30
CARD = 960          # kart boyutu (kare)
CARD_X, CARD_Y = 60, 400
TOTAL = 44.0
XF = 0.6            # geçiş süresi

# (başlangıç, kaynak, kaynak_saniye, crop x,y,w,h, arşiv mi)
SHOTS = [
    (0.0,  "v0", 65.0,  (96, 0, 288, 288),   True),   # genç Fahri Kuz mağaza kapısında
    (6.0,  "v0", 96.0,  (0, 9, 270, 270),    True),   # göz muayenesi (sepya)
    (11.0, "v0", 112.0, (40, 0, 288, 288),   True),   # mağaza önü grup + vitrin
    (14.6, "v0", 81.0,  (48, 0, 288, 288),   True),   # 30. yıl kitabı
    (18.4, "v0", 618.0, (100, 62, 184, 184), True),   # 90'lar, Fahri Kuz mağazada
    (22.4, "v2", 32.0,  (90, 30, 300, 300),  False),  # bugün, Fahri Kuz
    (26.4, "v2", 52.2,  (0, 0, 360, 360),    False),  # "Fahri Kuz 1960" imza
    (30.0, "v2", 73.2,  (100, 0, 300, 300),  False),  # alıntı: b-roll + Fahri Kuz konuşuyor
    (38.1, None, 0,     None,                False),  # kapanış kartı (siyah)
]

def run(cmd):
    print(" ".join(str(c) for c in cmd)[:300], flush=True)
    subprocess.run(cmd, check=True)

def build_shots():
    clips = []
    offsets = []
    for i, (start, src, ss, crop, archive) in enumerate(SHOTS):
        nxt = SHOTS[i + 1][0] if i + 1 < len(SHOTS) else None
        clip_start = 0.0 if i == 0 else start - XF / 2
        clip_end = (nxt + XF / 2) if nxt is not None else TOTAL
        dur = clip_end - clip_start
        out = WORK / f"shot_{i:02d}.mp4"
        if src is None:
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                 f"color=c=0x0f0c09:s={CARD}x{CARD}:r={FPS}:d={dur:.3f}",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(out)])
        else:
            x, y, w, h = crop
            # yavaş yakınlaşma (%0 → %7), titreşimi önlemek için 2 kat büyük çözünürlükte
            big = int(CARD * 1.25) // 2 * 2
            frames = int(dur * FPS)
            zoom = (f"zoompan=z='1+0.07*on/{frames}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                    f"s={CARD}x{CARD}:fps={FPS}")
            look = ("eq=contrast=1.04:saturation=0.85,vignette=PI/4.5"
                    if archive else "eq=contrast=1.03:saturation=1.0,vignette=PI/6")
            vf = (f"crop={w}:{h}:{x}:{y},scale={big}:{big}:flags=lanczos,{zoom},{look},"
                  f"setpts=N/{FPS}/TB,fps={FPS},setsar=1,format=yuv420p")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur:.3f}",
                 "-i", str(SRC / f"{src}.mp4"), "-an", "-vf", vf, "-t", f"{dur:.3f}",
                 "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", str(out)])
        clips.append((out, dur))
        if nxt is not None:
            offsets.append(nxt - XF / 2)
    return clips, offsets

def chain(clips, offsets):
    inputs = []
    for c, _ in clips:
        inputs += ["-i", str(c)]
    parts = []
    prev = "[0:v]"
    for i, off in enumerate(offsets):
        label = f"[x{i}]"
        parts.append(f"{prev}[{i+1}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{label}")
        prev = label
    out = WORK / "kart.mp4"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts),
         "-map", prev, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(out)])
    return out

def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def subtitles():
    gold = "&H006A9BB8"  # BGR, #B89B6A
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Header,Cormorant Garamond SemiBold,46,{gold},&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,14,0,1,0,0,8,60,60,250,1
Style: Sub,Cormorant Garamond Medium,66,&H00F2F2F2,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,0,3,8,90,90,1410,1
Style: Speaker,Cormorant Garamond Medium Italic,44,{gold},&H000000FF,&H00000000,&H00000000,0,1,0,0,100,100,2,0,1,0,0,8,90,90,1400,1
Style: Quote,Cormorant Garamond Medium Italic,64,&H00F2F2F2,&H000000FF,&H00000000,&H64000000,0,1,0,0,100,100,0,0,1,0,3,8,90,90,1470,1
Style: Title,Cormorant Garamond SemiBold,150,&H00F2F2F2,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,5,60,60,0,1
Style: Tagline,Cormorant Garamond Medium Italic,62,{gold},&H000000FF,&H00000000,&H00000000,0,1,0,0,100,100,1,0,1,0,0,5,60,60,0,1
Style: Small,Cormorant Garamond SemiBold,38,&H00BFBFBF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,16,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    fade = r"{\fad(300,300)}"
    ev = []
    def add(st, en, style, text, extra=""):
        ev.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},{style},,0,0,0,,{fade}{extra}{text}")
    add(0.3, 37.9, "Header", "YARIM  ASIR")
    add(1.0, 4.9, "Sub", "Yarım asır önce, Aksaray'da\\Nküçük bir gözlükçü dükkânı açıldı.")
    add(6.3, 10.9, "Sub", "Gözler ölçüldü, camlar kesildi,\\Nher çerçeve bir yüze göre ayarlandı.")
    add(13.8, 18.2, "Sub", "Yıllar içinde o dükkân, İstanbul'un\\Ndört bir yanına yayılan bir zincire dönüştü.")
    add(22.6, 27.0, "Sub", "Ve o usta, Fahri Kuz, bugün hâlâ\\Naynı tutkuyla gözlük tasarlıyor.")
    add(30.1, 37.9, "Speaker", "Fahri Kuz")
    add(30.2, 34.2, "Quote", "“Biz önce bir optisyeniz, sonra\\Ngözlük konusunda bir danışmanız,")
    add(34.3, 37.9, "Quote", "ne tip yüze ne tip gözlük uyacağı\\Nkonusunda bir estetisyeniz.”")
    # kapanış kartı
    add(38.6, 44.0, "Title", "Yarım Asır", r"{\pos(540,880)}")
    add(39.4, 44.0, "Tagline", "Bir gözlükçünün hikâyesi", r"{\pos(540,1010)}")
    add(40.4, 44.0, "Small", "BÖLÜM  1", r"{\pos(540,1130)}")
    add(41.4, 44.0, "Small", "DAMLA KUZ OPTİK", r"{\pos(540,1700)}")
    p = WORK / "altyazi.ass"
    p.write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    return p

def compose(kart, ass):
    out = WORK / "video_sessiz.mp4"
    fc = (
        f"color=c=0x0f0c09:s=1080x1920:r={FPS}:d={TOTAL},format=yuv420p[bg];"
        f"[bg]drawbox=x={CARD_X-3}:y={CARD_Y-3}:w={CARD+6}:h={CARD+6}:color=0xB89B6A@0.55:t=2:enable='lt(t,38.0)'[bgb];"
        f"[0:v]setpts=PTS-STARTPTS[k];"
        f"[bgb][k]overlay=x={CARD_X}:y={CARD_Y}:shortest=1[v1];"
        f"[v1]noise=alls=5:allf=t,subtitles={ass}:fontsdir={FONTS},fade=t=in:st=0:d=0.8,fade=t=out:st={TOTAL-0.8}:d=0.8[v]"
    )
    run(["ffmpeg", "-v", "error", "-y", "-i", str(kart), "-filter_complex", fc, "-map", "[v]",
         "-t", f"{TOTAL}", "-c:v", "libx264", "-crf", "22", "-preset", "medium", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", str(out)])
    return out

def audio():
    # anlatım cümleleri: (kaynak başlangıç, kaynak bitiş, hedef başlangıç)
    sentences = [(0.0, 3.50, 1.0), (3.86, 8.22, 6.3), (8.54, 12.72, 13.8),
                 (13.02, 17.26, 22.6), (17.69, 20.24, 38.8)]
    inputs = ["-i", str(WORK / "anlatim.mp3"), "-i", str(WORK / "izole.mp3"), "-i", str(WORK / "muzik.mp3")]
    parts, labels = [], []
    for i, (a, b, t) in enumerate(sentences):
        parts.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,"
                     f"afade=t=out:st={b-a-0.06:.2f}:d=0.06,adelay={int(t*1000)}:all=1[n{i}]")
        labels.append(f"[n{i}]")
    # Fahri Kuz alıntısı (müziği ayrıştırılmış kendi sesi; ses perdesi değiştirilmez)
    parts.append("[1:a]atrim=73.2:81.3,asetpts=PTS-STARTPTS,highpass=f=90,lowpass=f=9500,"
                 "afftdn=nr=8,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
                 "equalizer=f=3000:t=q:w=1.2:g=2,volume=1.6,"
                 "afade=t=in:d=0.12,afade=t=out:st=7.8:d=0.3,adelay=30000:all=1[q]")
    labels.append("[q]")
    voice = "".join(labels)
    parts.append(f"{voice}amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad=whole_dur={TOTAL}[vo]")
    parts.append(f"[2:a]atrim=0:{TOTAL},asetpts=PTS-STARTPTS,volume=0.55,"
                 f"afade=t=in:d=1.5,afade=t=out:st={TOTAL-3}:d=3[mu]")
    # anlatım sırasında müziği hafifçe kıs (sidechain)
    parts.append("[vo]asplit=2[vo1][vo2];[mu][vo2]sidechaincompress=threshold=0.03:ratio=4:attack=30:release=600[mud]")
    parts.append("[vo1][mud]amix=inputs=2:normalize=0:duration=longest,atrim=0:44,loudnorm=I=-14:TP=-1.0:LRA=11,aresample=48000[a]")
    out = WORK / "ses.m4a"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(parts), "-map", "[a]",
         "-t", f"{TOTAL}", "-c:a", "aac", "-b:a", "192k", str(out)])
    return out

def main():
    clips, offsets = build_shots()
    kart = chain(clips, offsets)
    ass = subtitles()
    v = compose(kart, ass)
    a = audio()
    run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-i", str(a), "-map", "0:v", "-map", "1:a",
         "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", "-shortest", str(OUT)])
    # altyazı dosyası (SRT) da ayrıca
    print("bitti:", OUT)

if __name__ == "__main__":
    main()
