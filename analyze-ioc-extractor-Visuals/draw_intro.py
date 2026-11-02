#!/usr/bin/env python3
"""analyze-ioc-extractor intro: the pier before the window opens. Wet pier boards close, three gull feathers
stuck flat by damp, anchor chain links running out of frame left, crate corner with rolled charts as plain
paper spirals, ticket booth dark except lamp glow leaking at the window seams, brass punch a dim shape on the
counter inside, tide tables as blank grey rectangles, mast flags hanging straight down, harbour water to a
lightless far shore, ferry at anchor with dark windows, clouded sky with no moon or stars. Nothing readable."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(53)
V1 = "--v1" in sys.argv
W, H = 1200, 520
NAVY = (12, 22, 44); GOLD = (196, 158, 74); GREEN = (110, 230, 160); GREY = (128, 132, 128)
img = Image.new("RGB", (W, H), (8, 16, 34)); d = ImageDraw.Draw(img, "RGBA")
# clouded night sky, no moon, no stars
for y in range(0, 170):
    t = y / 170; d.line([(0, y), (W, y)], fill=(int(8 + 5 * t), int(15 + 7 * t), int(32 + 9 * t)))
for _ in range(40):
    x, y = random.uniform(0, W), random.uniform(0, 130); d.ellipse([x, y, x + random.uniform(90, 220), y + 16], fill=(16, 26, 46, 120))
# harbour water, midnight navy, small knocking ripples against the piles
d.rectangle([0, 286, W, 400], fill=(10, 20, 40))
for _ in range(90):
    x, y = random.uniform(0, W), random.uniform(292, 394); ln = random.uniform(10, 42)
    d.line([(x, y), (x + ln, y)], fill=(30, 48, 78), width=2)
# far shore with no lights on it
d.rectangle([0, 268, W, 288], fill=(7, 12, 24))
# ferry shape at anchor, cabin windows DARK
d.polygon([(742, 246), (1050, 246), (1022, 268), (770, 268)], fill=(13, 20, 36))
d.rectangle([800, 222, 990, 246], fill=(15, 23, 40))
for i in range(6):
    x = 818 + i * 27; d.rectangle([x, 230, x + 16, 240], fill=(10, 15, 28))
d.line([(896, 196), (896, 222)], fill=(13, 20, 36), width=4)
# ticket booth midground left of centre, in darkness
d.rectangle([120, 150, 470, 400], fill=(18, 24, 34))
d.polygon([(100, 152), (295, 108), (492, 152)], fill=(12, 16, 26))  # roof
d.rectangle([168, 196, 330, 316], outline=(52, 58, 62), width=4)  # window frame
# lamp glow leaking at the window seams only: thin green lines at the joins, brighter in the shipped draft
glow = 200 if not V1 else 70
d.line([(168, 196), (330, 196)], fill=GREEN + (glow,), width=3); d.line([(168, 316), (330, 316)], fill=GREEN + (glow,), width=3)
d.line([(168, 196), (168, 316)], fill=GREEN + (int(glow * .7),), width=2); d.line([(330, 196), (330, 316)], fill=GREEN + (int(glow * .7),), width=2)
d.rectangle([172, 200, 326, 312], fill=(16, 30, 30))  # dark glass
# brass punch a dim shape on the counter inside, seen through the glass
d.line([(206, 282), (268, 252)], fill=(120, 96, 46), width=5); d.line([(206, 282), (262, 292)], fill=(110, 88, 42), width=5)
d.ellipse([258, 244, 282, 264], outline=(140, 112, 54), width=3)
# tide tables pinned under the eaves: blank grey rectangles, no figures
for i in range(3):
    x = 356 + i * 2; d.rectangle([352, 168 + i * 0, 352, 168], fill=GREY)
for i, x in enumerate((356, 396, 436)):
    if x + 30 < 470: d.rectangle([x, 166, x + 28, 204], fill=(104, 108, 104))
# short mast above the roof, flags hanging straight down
d.line([(430, 40), (430, 150)], fill=(24, 28, 36), width=5)
for i, col in enumerate(((30, 44, 66), (52, 60, 52), (44, 40, 30))):
    y = 52 + i * 30; d.polygon([(430, y), (462, y + 4), (460, y + 26), (430, y + 22)], fill=col)
# crate corner at right holding rolled charts, ends as plain spirals of paper
d.rectangle([952, 300, 1180, 400], fill=(86, 84, 78)); d.rectangle([952, 300, 1180, 318], fill=(102, 100, 92))
for (x, y, r) in [(1000, 282, 22), (1052, 276, 25), (1108, 284, 20)]:
    d.ellipse([x - r, y - r, x + r, y + r], fill=(196, 190, 168))
    for rr in (r * .66, r * .33):
        d.arc([x - rr, y - rr, x + rr, y + rr], 20, 320, fill=(150, 144, 124), width=2)
# foreground: wet pier boards at close focus with damp sheen
d.rectangle([0, 400, W, H], fill=(52, 46, 38))
for ly in range(414, H, 26):
    d.line([(0, ly), (W, ly + 3)], fill=(38, 33, 26), width=4)
for _ in range(46):
    x, y = random.uniform(0, W), random.uniform(404, H); d.ellipse([x, y, x + random.uniform(20, 60), y + 4], fill=(90, 104, 116, 60))
# anchor chain lower links running out of the frame at the left
for i in range(4):
    x, y = -18 + i * 56, 452 - i * 6
    d.ellipse([x, y, x + 62, y + 34], outline=(96, 98, 96), width=8)
# three gull feathers lying flat where the damp stuck them down
def feather(x, y, ang, ln):
    ex, ey = x + math.cos(ang) * ln, y + math.sin(ang) * ln
    d.line([(x, y), (ex, ey)], fill=(206, 208, 200), width=3)
    for t in (.25, .45, .65, .85):
        bx, by = x + (ex - x) * t, y + (ey - y) * t; s = 13 * (1 - t * .4)
        d.line([(bx, by), (bx - s * .5, by - s)], fill=(186, 190, 182), width=2)
        d.line([(bx, by), (bx + s, by - s * .3)], fill=(196, 200, 192), width=2)
feather(300, 470, -0.3, 92); feather(560, 492, 0.15, 78); feather(838, 462, -0.9, 84)
img = img.filter(ImageFilter.GaussianBlur(0.6))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
