#!/usr/bin/env python3
"""analyze-ioc-extractor wordmark banner: the last crossing of the night from the pier side of a lamplit
ticket booth, right of centre, window glowing phosphor green, tide tables pinned under the eaves, rolled
charts in a weathered grey crate by the door. Foreground counter carries the brass ticket punch larger than
anything else, beside a fan of punched stubs, a stub book, and a coil of anchor chain as a paperweight.
Through the open lower window the harbour water carries one lit ferry at a distance. Gull feathers on the
pier boards, signal flags slack on a short mast. The office name is painted glass lettering in Briem Hand
in rope gold across the booth window, one line only, no other readable writing anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(57)
V1 = "--v1" in sys.argv
W, H = 1200, 420
NAVY = (10, 20, 40); GOLD = (196, 158, 74); GREEN = (110, 230, 160); GREY = (128, 132, 128)
img = Image.new("RGB", (W, H), (7, 14, 30)); d = ImageDraw.Draw(img, "RGBA")
# harbour water across the back, one lit ferry at a distance moving slowly
d.rectangle([0, 150, W, 300], fill=(9, 18, 36))
for _ in range(60):
    x, y = random.uniform(0, W), random.uniform(160, 290); d.line([(x, y), (x + random.uniform(12, 40), y)], fill=(28, 44, 72), width=2)
d.polygon([(96, 208), (330, 208), (306, 230), (122, 230)], fill=(16, 24, 44))
d.rectangle([140, 184, 288, 208], fill=(18, 27, 48))
for i in range(5):
    x = 154 + i * 26; d.rectangle([x, 192, x + 15, 202], fill=(244, 226, 160))
d.line([(214, 160), (214, 184)], fill=(16, 24, 44), width=4); d.ellipse([208, 148, 220, 160], fill=(250, 232, 160))
# pier boards foreground
d.rectangle([0, 300, W, H], fill=(54, 48, 40))
for ly in range(314, H, 24):
    d.line([(0, ly), (W, ly + 3)], fill=(40, 35, 28), width=3)
# ticket booth right of centre
d.rectangle([648, 84, 1050, 330], fill=(22, 28, 38))
d.polygon([(628, 86), (849, 44), (1070, 86)], fill=(14, 18, 28))
# window glowing phosphor green from the lamp inside
d.rectangle([692, 118, 936, 262], fill=(24, 66, 48)); d.rectangle([692, 118, 936, 262], outline=(70, 74, 70), width=5)
d.rectangle([692, 196, 936, 262], fill=(30, 84, 58))  # open lower half, brighter
try:
    fg = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BriemHand.ttf", 44)
except Exception:
    fg = ImageFont.load_default()
if not V1:  # painted glass lettering across the booth window, one line only
    d.text((814, 158), "analyze-ioc-extractor", font=fg, fill=GOLD, anchor="mm")
else:  # draft 1 flaw: name set as a paper sign nailed over the booth door, not painted glass
    d.rectangle([952, 130, 1180, 176], fill=(210, 204, 182)); d.text((1066, 153), "analyze-ioc-extractor", font=ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/BriemHand.ttf", 25), fill=(20, 26, 40), anchor="mm")
# tide tables pinned in a row under the eaves: pale rectangles, figures too small to read, kept abstract
for i in range(4):
    x = 700 + i * 62; d.rectangle([x, 92, x + 46, 112], fill=(168, 170, 162))
# rolled charts upright in a weathered grey crate by the door
d.rectangle([962, 268, 1050, 330], fill=(96, 96, 90)); d.rectangle([962, 268, 1050, 282], fill=(112, 112, 104))
for (x, r) in [(982, 13), (1006, 15), (1030, 12)]:
    d.ellipse([x - r, 236 - r, x + r, 236 + r], fill=(198, 192, 170)); d.arc([x - r * .55, 236 - r * .55, x + r * .55, 236 + r * .55], 20, 320, fill=(152, 146, 126), width=2)
d.rectangle([962, 118, 1050, 268], outline=(52, 56, 54), width=4)  # door outline
# short mast above the roof, signal flags hanging slack
d.line([(1058, 8), (1058, 86)], fill=(26, 30, 38), width=4)
for i, col in enumerate((GREEN, GOLD, GREY)):
    y = 16 + i * 22; d.polygon([(1058, y), (1086, y + 3), (1084, y + 18), (1058, y + 15)], fill=col)
# counter in the foreground, larger than anything else: the brass ticket punch at rest
d.rectangle([0, 330, 648, H], fill=(66, 58, 46))
px, py = 268, 366
d.line([(px, py), (96, 330)], fill=GOLD, width=10); d.line([(px, py), (104, 404)], fill=GOLD, width=10)
d.line([(px, py), (470, 348)], fill=GOLD, width=12); d.line([(px, py), (466, 388)], fill=GOLD, width=12)
d.ellipse([px - 13, py - 13, px + 13, py + 13], fill=(228, 192, 106), outline=(140, 110, 50), width=3)
d.polygon([(462, 338), (566, 346), (566, 392), (462, 398)], fill=(214, 208, 188))
d.ellipse([494, 356, 524, 386], fill=GREEN)
# fan of punched stubs beside the punch
for i, ang in enumerate((-24, -8, 8, 24)):
    a = math.radians(ang); cx0, cy0 = 150 + i * 6, 396
    pts = [(cx0 + dx * math.cos(a) - dy * math.sin(a), cy0 + dx * math.sin(a) + dy * math.cos(a)) for (dx, dy) in [(-46, -15), (46, -15), (46, 15), (-46, 15)]]
    d.polygon(pts, fill=(200, 194, 172), outline=(152, 146, 124)); d.ellipse([cx0 - 8, cy0 - 8, cx0 + 8, cy0 + 8], fill=GREEN)
# stub book: a bound grey book with punched holes along its edge
d.rectangle([330, 384, 470, 416], fill=(104, 106, 100)); d.rectangle([330, 384, 470, 392], fill=(140, 142, 134))
for x in (348, 380, 412, 444):
    d.ellipse([x, 396, x + 9, 405], fill=GREEN)
# coil of anchor chain used as a paperweight
for i in range(3):
    d.ellipse([540 + i * 4, 372 - i * 9, 612 + i * 4, 402 - i * 9], outline=(100, 102, 98), width=7)
# gull feathers scattered on the pier boards near the booth steps
def feather(x, y, ang, ln):
    ex, ey = x + math.cos(ang) * ln, y + math.sin(ang) * ln
    d.line([(x, y), (ex, ey)], fill=(206, 208, 200), width=3)
    for t in (.3, .55, .8):
        bx, by = x + (ex - x) * t, y + (ey - y) * t
        d.line([(bx, by), (bx - 6, by - 11)], fill=(188, 192, 184), width=2); d.line([(bx, by), (bx + 11, by - 4)], fill=(198, 202, 194), width=2)
feather(700, 356, -0.4, 62); feather(880, 388, 0.2, 54); feather(1086, 352, -1.0, 58)
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
