# Yarım Asır, Bölüm 1 (HyperFrames projesi)

- `hazirla.sh <kaynak>`: Topaz ile netleştirilmiş kare/klipleri renklendirir, 9:16 kırpar, gren ekler ve ses miksini (`assets/audio/miks.m4a`) üretir. Kaynak dosyalar Drive > "Claude çalışma dosyaları" ve ElevenLabs akışındadır.
- `olustur_index.py`: `index.html`'i üretir. Zamanlamalar, altyazı kelime zamanları ve metinler burada tek yerde durur. Elle `index.html` düzenlemek yerine bu dosyayı değiştirip yeniden çalıştırın.
- Render: `npx --yes hyperframes@0.9.72 render -o ../cikti/<ad>.mp4 --max-bitrate 14M`
- Ses: anlatım ElevenLabs (Cem), Fahri Kuz'un kendi sesi (tanıtım filminden, müzik ayrıştırılmış), enstrümantal müzik ve efektler (ElevenLabs).
- GSAP CDN bu ortamda kapalı olduğu için `assets/gsap.min.js` yereldir.
