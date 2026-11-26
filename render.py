#!/usr/bin/env python3
"""Render the front page for THE WORLD TODAY - Thursday 26 November 2026.

Draws a 1024x1024 newspaper front page with Pillow only. Deterministic:
same input, same bytes. Run: python3 render.py  ->  entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 228)
INK = (18, 18, 18)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
GREY = (90, 86, 76)
LIGHT_LINE = (120, 112, 96)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, leading, fill=INK, align="left"):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_refinery_scene(d, x0, y0, x1, y1):
    """Wide dusk scene: refinery towers under a rising black smoke plume.

    Everything is placed relative to the panel so nothing escapes it:
    ground top = y1-52, towers <= 85 tall, plume rises <= 94 above its base.
    """
    d.rectangle([x0, y0, x1, y1], fill=(232, 196, 138))
    ground = y1 - 52
    # sun low on the horizon
    d.ellipse([x1 - 150, y0 + 22, x1 - 90, y0 + 82], fill=(214, 110, 44))
    # ground
    d.rectangle([x0, ground, x1, y1], fill=(74, 66, 58))
    # storage tanks
    for tx, tw, th in [(x0 + 30, 92, 52), (x0 + 138, 76, 44), (x0 + 228, 84, 48)]:
        d.rectangle([tx, ground - th, tx + tw, ground], fill=(196, 188, 172),
                    outline=INK, width=2)
        d.ellipse([tx - 3, ground - th - 8, tx + tw + 3, ground - th + 6],
                  fill=(214, 206, 188), outline=INK, width=2)
    # distillation towers (short, so the plume fits above them)
    for tx, tw, th in [(x0 + 350, 26, 70), (x0 + 392, 20, 55), (x0 + 428, 30, 85)]:
        d.rectangle([tx, ground - th, tx + tw, ground], fill=(158, 150, 136),
                    outline=INK, width=2)
        d.rectangle([tx - 4, ground - th - 10, tx + tw + 4, ground - th],
                    fill=(120, 112, 98), outline=INK, width=2)
    # flare stack: a short stack with a flame teardrop, low and to the right
    fx = x0 + 560
    d.rectangle([fx, ground - 34, fx + 14, ground], fill=(120, 112, 98),
                outline=INK, width=2)
    d.polygon([(fx - 4, ground - 34), (fx - 2, ground - 58), (fx + 7, ground - 46),
               (fx + 12, ground - 66), (fx + 18, ground - 44), (fx + 20, ground - 34)],
              fill=(232, 120, 30), outline=(163, 22, 33))
    # pipe run
    d.line([(x0 + 30, ground - 16), (x0 + 470, ground - 16)], fill=INK, width=3)
    # black smoke plume rising from the tallest tower (x0+443, top ground-85),
    # drifting left as it rises so it reads as smoke, not a pillar
    sx = x0 + 443
    base = ground - 85 - 4
    for i, r in enumerate([24, 28, 30, 26, 20]):
        cx = sx - i * 12
        cy = base - i * 17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(35, 32, 30))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def draw_tanker(d, x0, y0):
    """Oil tanker on waves with a naval mine."""
    d.rectangle([x0, y0, x0 + 150, y0 + 96], fill=(214, 228, 232))
    d.rectangle([x0, y0, x0 + 150, y0 + 96], outline=INK, width=2)
    d.polygon([(x0 + 12, y0 + 52), (x0 + 138, y0 + 52), (x0 + 128, y0 + 74),
               (x0 + 22, y0 + 74)], fill=(163, 22, 33), outline=INK)
    d.rectangle([x0 + 96, y0 + 28, x0 + 126, y0 + 52], fill=(247, 242, 228),
                outline=INK, width=2)
    d.rectangle([x0 + 20, y0 + 40, x0 + 88, y0 + 52], fill=(90, 86, 76),
                outline=INK, width=2)
    d.rectangle([x0 + 108, y0 + 16, x0 + 118, y0 + 28], fill=(29, 78, 137),
                outline=INK, width=2)
    mx, my = x0 + 128, y0 + 18
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(18, 18, 18))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx + 9 * math.cos(a), my + 9 * math.sin(a)),
                (mx + 15 * math.cos(a), my + 15 * math.sin(a))],
               fill=INK, width=2)
    for wy in (y0 + 82, y0 + 90):
        d.arc([x0 + 6, wy - 6, x0 + 40, wy + 6], 0, 180, fill=BLUE, width=2)
        d.arc([x0 + 58, wy - 6, x0 + 92, wy + 6], 0, 180, fill=BLUE, width=2)
        d.arc([x0 + 110, wy - 6, x0 + 144, wy + 6], 0, 180, fill=BLUE, width=2)


def draw_gaza_building(d, x0, y0):
    d.rectangle([x0, y0, x0 + 150, y0 + 96], fill=(226, 214, 188))
    d.rectangle([x0, y0, x0 + 150, y0 + 96], outline=INK, width=2)
    d.polygon([(x0 + 28, y0 + 14), (x0 + 118, y0 + 14), (x0 + 118, y0 + 82),
               (x0 + 28, y0 + 82)], fill=(196, 182, 158), outline=INK, width=2)
    d.polygon([(x0 + 118, y0 + 14), (x0 + 136, y0 + 30), (x0 + 118, y0 + 44)],
              fill=(247, 242, 228), outline=INK, width=2)
    for wy in (y0 + 26, y0 + 44, y0 + 62):
        for wx in (x0 + 40, x0 + 64, x0 + 88):
            d.rectangle([wx, wy, wx + 14, wy + 10], fill=(247, 242, 228),
                        outline=INK, width=1)
    d.polygon([(x0 + 96, y0 + 82), (x0 + 150, y0 + 82), (x0 + 150, y0 + 96),
               (x0 + 118, y0 + 96), (x0 + 112, y0 + 88)], fill=(120, 112, 98))
    for cx, cy, r in [(x0 + 128, y0 + 18, 10), (x0 + 138, y0 + 8, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 86, 76))


def draw_ukraine_flame(d, x0, y0):
    d.rectangle([x0, y0, x0 + 150, y0 + 96], fill=(214, 228, 232))
    d.rectangle([x0, y0, x0 + 150, y0 + 96], outline=INK, width=2)
    d.rectangle([x0 + 18, y0 + 52, x0 + 132, y0 + 82], fill=(90, 86, 76),
                outline=INK, width=2)
    d.rectangle([x0 + 30, y0 + 30, x0 + 44, y0 + 52], fill=(120, 112, 98),
                outline=INK, width=2)
    d.rectangle([x0 + 96, y0 + 22, x0 + 108, y0 + 52], fill=(120, 112, 98),
                outline=INK, width=2)
    d.polygon([(x0 + 60, y0 + 52), (x0 + 52, y0 + 26), (x0 + 64, y0 + 34),
               (x0 + 72, y0 + 14), (x0 + 82, y0 + 36), (x0 + 92, y0 + 28),
               (x0 + 88, y0 + 52)], fill=(232, 120, 30), outline=(163, 22, 33))
    for cx, cy, r in [(x0 + 102, y0 + 14, 9), (x0 + 112, y0 + 8, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(35, 32, 30))


def draw_supermarket(d, x0, y0):
    d.rectangle([x0, y0, x0 + 150, y0 + 96], fill=(226, 214, 188))
    d.rectangle([x0, y0, x0 + 150, y0 + 96], outline=INK, width=2)
    d.rectangle([x0 + 20, y0 + 26, x0 + 130, y0 + 84], fill=(247, 242, 228),
                outline=INK, width=2)
    for i in range(6):
        x = x0 + 20 + i * 18
        d.rectangle([x, y0 + 26, x + 18, y0 + 40],
                    fill=RED if i % 2 == 0 else (247, 242, 228))
    d.rectangle([x0 + 20, y0 + 26, x0 + 130, y0 + 40], outline=INK, width=2)
    d.rectangle([x0 + 62, y0 + 48, x0 + 88, y0 + 84], fill=(29, 78, 137),
                outline=INK, width=2)
    d.ellipse([x0 + 70, y0 + 56, x0 + 80, y0 + 66], fill=(247, 242, 228),
              outline=INK, width=2)
    d.polygon([(x0 + 118, y0 + 52), (x0 + 132, y0 + 58), (x0 + 132, y0 + 70),
               (x0 + 118, y0 + 78), (x0 + 104, y0 + 70), (x0 + 104, y0 + 58)],
              fill=(29, 78, 137), outline=INK, width=2)
    d.text((x0 + 112, y0 + 60), "✓", font=font(SANS_B, 16), fill=(247, 242, 228))


def draw_garment(d, x0, y0):
    d.rectangle([x0, y0, x0 + 150, y0 + 96], fill=(214, 228, 232))
    d.rectangle([x0, y0, x0 + 150, y0 + 96], outline=INK, width=2)
    d.line([(x0 + 75, y0 + 14), (x0 + 75, y0 + 26)], fill=INK, width=3)
    d.arc([x0 + 68, y0 + 8, x0 + 82, y0 + 20], 180, 360, fill=INK, width=3)
    d.polygon([(x0 + 75, y0 + 26), (x0 + 44, y0 + 38), (x0 + 34, y0 + 62),
               (x0 + 50, y0 + 62), (x0 + 50, y0 + 84), (x0 + 100, y0 + 84),
               (x0 + 100, y0 + 62), (x0 + 116, y0 + 62), (x0 + 106, y0 + 38)],
              fill=(29, 78, 137), outline=INK, width=2)
    d.line([(x0 + 112, y0 + 78), (x0 + 128, y0 + 56), (x0 + 140, y0 + 62)],
           fill=RED, width=4)
    d.line([(x0 + 112, y0 + 78), (x0 + 128, y0 + 56)], fill=RED, width=4)
    d.polygon([(x0 + 128, y0 + 50), (x0 + 138, y0 + 58), (x0 + 126, y0 + 62)],
              fill=RED)
    d.rectangle([x0 + 18, y0 + 64, x0 + 34, y0 + 84], fill=(232, 120, 30),
                outline=INK, width=2)


def icon_image(draw_fn):
    """Render one 150x96 icon function into a small image, scaled to 110x70."""
    im = Image.new("RGB", (150, 96), PAPER)
    draw_fn(ImageDraw.Draw(im), 0, 0)
    return im.resize((110, 70), Image.LANCZOS)


def story_cell(img, d, x, y, w, h, kicker, headline, summary, draw_icon):
    d.rectangle([x, y, x + w, y + h], outline=LIGHT_LINE, width=1)
    d.rectangle([x + 10, y + 8, x + 10 + 110, y + 8 + 70], outline=INK, width=1)
    img.paste(icon_image(draw_icon), (x + 10, y + 8))
    tx = x + 128
    d.text((tx, y + 10), kicker, font=font(SANS_B, 12), fill=RED)
    text_block(d, tx, y + 28, headline, font(SANS_B, 16), w - 138, 19)
    text_block(d, x + 10, y + 88, summary, font(SANS, 13), w - 20, 16,
               fill=(50, 48, 44))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=INK, width=1)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 60)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    rule(d, 40, 108, W - 40, 3)
    rule(d, 40, 113, W - 40, 1)
    dateline = "THURSDAY, 26 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE"
    df = font(SANS_B, 16)
    d.text(((W - d.textlength(dateline, font=df)) / 2, 122), dateline, font=df,
           fill=INK)

    # ---- lead story ----
    y = 152
    d.text((40, y), "MIDDLE EAST  ·  LEAD STORY", font=font(SANS_B, 15), fill=RED)
    y += 26
    y = text_block(d, 40, y,
                   "Houthis claim strike on Saudi Arabia's biggest refinery",
                   font(SERIF_B, 38), W - 80, 44)
    y += 4
    y = text_block(
        d, 40, y,
        "Satellite images show thick black smoke over Ras Tanura, the kingdom's "
        "largest refinery, after the Houthis say they hit it — as Brent crude jumps "
        "and the Saudi-led coalition says its defences downed four drones.",
        font(SANS, 16), W - 80, 21, fill=(50, 48, 44))
    y += 10
    draw_refinery_scene(d, 40, y, W - 40, y + 240)
    y += 240 + 12
    rule(d, 40, y, W - 40, 2)
    y += 12

    # ---- five more stories ----
    gap = 14
    col_w = (W - 80 - 2 * gap) // 3
    row_h = 170
    stories = [
        ("SHIPPING · HORMUZ",
         "Two tankers hit naval mines",
         "Iran's navy says an LNG carrier and an oil tanker struck mines and caught "
         "fire. Tehran says the strait stays shut until its demands are met.",
         draw_tanker),
        ("GAZA · CEASEFIRE",
         "Israel kills Hamas security chief",
         "An airstrike in Gaza City kills Mohammad Abuelouf, Hamas' internal security "
         "chief for northern Gaza, with his wife and two daughters — the second senior "
         "Hamas security official killed in a day.",
         draw_gaza_building),
        ("UKRAINE · OIL WAR",
         "Ukraine hits Russian refineries",
         "Kyiv's drones strike Russian oil refineries again and Moscow vows "
         "retaliation, as Russia's own figures show nearly 500,000 war dead.",
         draw_ukraine_flame),
        ("COLOMBIA · CARTAGENA",
         "Police free 20 supermarket hostages",
         "After 17 hours, police storm a Cartagena supermarket and free 20 people "
         "held by gunmen following a failed armoured-truck robbery.",
         draw_supermarket),
        ("ASIA · BANGLADESH",
         "Garment workers win 36% pay rise",
         "Bangladesh raises the minimum monthly wage for entry-level garment workers "
         "by 36%, a win for millions in the world's second-biggest clothing exporter.",
         draw_garment),
    ]
    for i in range(3):
        story_cell(img, d, 40 + i * (col_w + gap), y, col_w, row_h, *stories[i])
    y += row_h + gap
    col2_w = (W - 80 - gap) // 2
    for i in range(3, 5):
        story_cell(img, d, 40 + (i - 3) * (col2_w + gap), y, col2_w, row_h,
                   *stories[i])
    y += row_h + 10
    rule(d, 40, y, W - 40, 1, fill=LIGHT_LINE)
    foot = ("Compiled from wire reports (Reuters, AP, Xinhua) published on 26 November 2026  ·  "
            "make.fun news-image-20261126")
    ff = font(SANS, 13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y + 8), foot, font=ff,
           fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
