"""Adaptive launcher icon for NFSMW Android Evolved from assets/icon/icono.png (round artwork, transparent corners).

Foreground: the artwork without its thin black outer ring, its circle covering 74 % of the 108 dp canvas (just past the
72 dp a launcher shows, so the text is whole), on the same artwork enlarged and blurred that fills the rest.
Background: the same artwork enlarged and blurred, in case a mask shows the canvas corners.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

repo = sys.argv[1]
src = Image.open(os.path.join(repo, 'assets/icon/icono.png')).convert('RGBA')
w, h = src.size
# Drop the outer ring (about 1 % of the radius) with an antialiased circular mask.
ring = int(w * 0.012)
art = src.crop((ring, ring, w - ring, h - ring))
mask = Image.new('L', (art.width * 4, art.height * 4), 0)
ImageDraw.Draw(mask).ellipse((0, 0, mask.width - 1, mask.height - 1), fill=255)
mask = mask.resize(art.size, Image.LANCZOS)
art.putalpha(Image.composite(art.getchannel('A'), Image.new('L', art.size, 0), mask))

res = os.path.join(repo, 'android/app/src/main/res')
densidades = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
for nombre, lado in densidades.items():
    carpeta = os.path.join(res, f'mipmap-{nombre}')
    os.makedirs(carpeta, exist_ok=True)
    # Foreground: the circle at 74 % of the canvas, centred.
    d = round(lado * 0.74)
    frente = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
    frente.alpha_composite(art.resize((d, d), Image.LANCZOS), ((lado - d) // 2, (lado - d) // 2))
    frente.save(os.path.join(carpeta, 'ic_launcher_foreground.png'), optimize=True)
    # Background: the artwork at 160 %, blurred, opaque.
    g = round(lado * 1.6)
    fondo = Image.new('RGBA', (lado, lado), (8, 12, 18, 255))
    grande = art.resize((g, g), Image.LANCZOS).filter(ImageFilter.GaussianBlur(lado * 0.04))
    fondo.alpha_composite(grande, ((lado - g) // 2, (lado - g) // 2))
    fondo.convert('RGB').save(os.path.join(carpeta, 'ic_launcher_background.png'), optimize=True)

anydpi = os.path.join(res, 'mipmap-anydpi-v26')
os.makedirs(anydpi, exist_ok=True)
xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
       '<!-- Adaptive icon (Android 8+): the artwork fills the launcher shape (tools/icono/icono_adaptativo.py). -->\n'
       '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
       '    <background android:drawable="@mipmap/ic_launcher_background" />\n'
       '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n'
       '    <monochrome android:drawable="@mipmap/ic_launcher_foreground" />\n'
       '</adaptive-icon>\n')
open(os.path.join(anydpi, 'ic_launcher.xml'), 'w', encoding='utf-8').write(xml)

# A preview of what a circle and a squircle launcher show (central 72 dp of 108).
lado = 432
vista = Image.new('RGBA', (lado * 2 + 40, lado), (255, 255, 255, 255))
for k, forma in enumerate(('circle', 'squircle')):
    capa = Image.open(os.path.join(res, 'mipmap-xxxhdpi/ic_launcher_background.png')).convert('RGBA')
    capa.alpha_composite(Image.open(os.path.join(res, 'mipmap-xxxhdpi/ic_launcher_foreground.png')))
    m = Image.new('L', (lado, lado), 0)
    a = lado * 18 // 108
    caja = (a, a, lado - a, lado - a)
    if forma == 'circle':
        ImageDraw.Draw(m).ellipse(caja, fill=255)
    else:
        ImageDraw.Draw(m).rounded_rectangle(caja, radius=lado * 22 // 108, fill=255)
    vista.paste(capa, (k * (lado + 40), 0), m)
vista.save(sys.argv[2])
print('ok')
