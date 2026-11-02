#!/usr/bin/env python3
"""analyze-ioc-extractor logo: brass ticket punch in profile on a flat midnight navy field, long handles
OPEN at rest, punching head turned to the viewer with its shaped die: a small clean circle bitten out of a
stub of ticket card still in the jaws. Rope gold outlines the punch and its pivot rivet, phosphor green
fills the punched hole and a short fanned stack of punched stubs beneath, weathered grey shades the spring
along the lower handle. Name underneath in Briem Hand in rope gold. No hand, no ferry, nothing else."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V1 = "--v1" in sys.argv
W, H = 900, 560
NAVY = (12, 22, 44); GOLD = (196, 158, 74); GREEN = (110, 230, 160); GREY = (128, 132, 128); STUB = (214, 208, 188)
img = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(img, "RGBA")
# pivot at centre left, head at right, handles opening to the left
px, py = 400, 218
if V1:  # draft 1 flaw: handles nearly shut, the tool reads as pliers
    up_end, low_end = (92, 178), (96, 262)
else:  # shipped: handles open at rest, jaws visibly apart
    up_end, low_end = (78, 108), (82, 336)
# upper handle and jaw
d.line([(px, py), up_end], fill=GOLD, width=13); d.line([(px, py), (640, 178)], fill=GOLD, width=15)
# lower handle and jaw
d.line([(px, py), low_end], fill=GOLD, width=13); d.line([(px, py), (640, 262)], fill=GOLD, width=15)
# handle grips shaded in weathered grey inside the gold outline
d.line([((px + up_end[0]) // 2, (py + up_end[1]) // 2), up_end], fill=(104, 106, 100), width=6)
d.line([((px + low_end[0]) // 2, (py + low_end[1]) // 2), low_end], fill=(104, 106, 100), width=6)
# spring along the lower handle in weathered grey: a small coil
for i in range(6):
    x = 236 + i * 22; d.arc([x, py + 62, x + 20, py + 92], 0, 300, fill=GREY, width=4)
# pivot rivet picked out in rope gold
d.ellipse([px - 17, py - 17, px + 17, py + 17], fill=(226, 190, 104), outline=(140, 110, 50), width=3)
d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(120, 94, 40))
# stub of ticket card still in the jaws, head turned to the viewer
d.polygon([(636, 168), (792, 182), (792, 258), (636, 272)], fill=STUB)
d.polygon([(636, 168), (792, 182), (792, 258), (636, 272)], outline=(168, 160, 138))
# the shaped die: a small clean circle bitten out of the stub, phosphor green through the hole
d.ellipse([692, 198, 730, 236], fill=GREEN); d.ellipse([692, 198, 730, 236], outline=(90, 84, 66), width=3)
# die face ring above the stub where the punch head meets it
d.ellipse([688, 158, 734, 192], outline=GOLD, width=5)
# short stack of already punched stubs fanned beneath the punch, each with its green hole
for i, ang in enumerate((-16, 0, 16)):
    a = math.radians(ang); cx0, cy0 = 520 + i * 44, 386
    pts = []
    for (dx, dy) in [(-58, -20), (58, -20), (58, 20), (-58, 20)]:
        pts.append((cx0 + dx * math.cos(a) - dy * math.sin(a), cy0 + dx * math.sin(a) + dy * math.cos(a)))
    d.polygon(pts, fill=(198, 192, 170), outline=(150, 144, 122))
    d.ellipse([cx0 - 10, cy0 - 10, cx0 + 10, cy0 + 10], fill=GREEN)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BriemHand.ttf", 52)
except Exception:
    f = ImageFont.load_default()
d.text((450, 492), "analyze-ioc-extractor", font=f, fill=GOLD, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if not V1:
    img.resize((103, 64)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
