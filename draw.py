#!/usr/bin/env python3
"""Build-time script: draw the 19 November 2026 world-news image (1024x1024).

Fresh original artwork for news-image-20261119. Run:
    python3 draw.py            # writes entry.png next to this file
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (245, 239, 227)      # warm off-white
INK = (23, 32, 58)           # dark navy ink
TEAL = (14, 124, 123)
CORAL = (228, 87, 46)
AMBER = (242, 165, 65)
BLUE = (46, 95, 163)
PURPLE = (108, 74, 176)
RED = (192, 57, 43)
GREY = (90, 96, 110)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, fnt, fill, leading=None):
    """Draw lines of text; return y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(d, x0, y0, x1, y1, fill=WHITE):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=INK, width=3)


def story_panel(d, x0, y0, x1, y1, kicker, kicker_color, headline, subline,
                art, headline_size=27, sub_size=16, art_frac=0.44):
    """A panel with a flat illustration on top and text below."""
    panel(d, x0, y0, x1, y1)
    art_h = int((y1 - y0) * art_frac)
    art(d, x0 + 3, y0 + 3, x1 - 3, y0 + art_h)
    d.line([x0 + 3, y0 + art_h, x1 - 3, y0 + art_h], fill=INK, width=3)
    tx = x0 + 16
    ty = y0 + art_h + 12
    tw = x1 - x0 - 32
    d.text((tx, ty), kicker, font=font(SANS_B, 15), fill=kicker_color)
    ty += 24
    hl = wrap(d, headline, font(SANS_B, headline_size), tw)
    ty = draw_text_block(d, tx, ty, hl, font(SANS_B, headline_size), INK,
                         leading=headline_size + 4)
    ty += 4
    sl = wrap(d, subline, font(SANS, sub_size), tw)
    end_y = draw_text_block(d, tx, ty, sl, font(SANS, sub_size), GREY,
                            leading=sub_size + 4)
    assert end_y <= y1 - 6, f"text overflows panel: {headline!r} ends {end_y} > {y1 - 6}"


# ---------- flat illustrations ----------

def art_gta(d, x0, y0, x1, y1):
    # sunset gradient bands: orange -> pink -> purple
    top, mid, bot = (255, 140, 66), (232, 93, 117), (108, 74, 176)
    h = y1 - y0
    for i in range(h):
        t = i / max(h - 1, 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(top[k] + (mid[k] - top[k]) * u) for k in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(mid[k] + (bot[k] - mid[k]) * u) for k in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=c)
    # sun
    cx, cy, r = (x0 + x1) // 2 - 60, y0 + h // 2 - 8, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 209, 102))
    # skyline silhouette
    base = y1
    sky = [(x0, 46), (x0 + 34, 46), (x0 + 34, 30), (x0 + 62, 30),
           (x0 + 62, 52), (x0 + 96, 52), (x0 + 96, 22), (x0 + 124, 22),
           (x0 + 124, 52), (x0 + 158, 52), (x0 + 158, 38), (x0 + 190, 38),
           (x0 + 190, 58), (x0 + 224, 58), (x0 + 224, 34), (x0 + 252, 34),
           (x0 + 252, 56), (x0 + 288, 56), (x0 + 288, 26), (x0 + 316, 26),
           (x0 + 316, 52), (x0 + 348, 52), (x0 + 348, 40), (x0 + 380, 40),
           (x0 + 380, 58), (x0 + 420, 58), (x0 + 420, 30), (x0 + 448, 30),
           (x0 + 448, 58), (x1, 58)]
    pts = [(x0, base)] + [(x, base - dy) for (x, dy) in sky] + [(x1, base)]
    d.polygon(pts, fill=(30, 20, 60))
    # palm silhouettes: curved fronds drooping from the trunk top
    for px, ph in ((x0 + 52, 52), (x1 - 46, 46)):
        top_y = base - ph
        d.line([px, base, px + 6, top_y], fill=(30, 20, 60), width=5)
        for ang in (-75, -40, -8, 28, 65):
            import math
            a = math.radians(ang - 90)
            ex = px + 6 + int(26 * math.cos(a))
            ey = top_y + int(26 * math.sin(a)) + 12
            mx = px + 6 + int(15 * math.cos(a))
            my = top_y + int(15 * math.sin(a)) - 4
            d.line([px + 6, top_y, mx, my, ex, ey], fill=(30, 20, 60),
                   width=4, joint="curve")


def art_capitol(d, x0, y0, x1, y1):
    # Fits a ~100px-tall art box: dome + pediment + columned building.
    d.rectangle([x0, y0, x1, y1], fill=(31, 58, 95))
    cx = (x0 + x1) // 2
    base = y1
    # white building block with navy columns
    d.rectangle([cx - 92, base - 52, cx + 92, base], fill=WHITE)
    for i in range(5):
        colx = cx - 72 + i * 30
        d.rectangle([colx, base - 44, colx + 12, base - 8], fill=(31, 58, 95))
    # pediment triangle above the columns
    d.polygon([(cx - 92, base - 52), (cx + 92, base - 52), (cx, base - 64)],
              fill=WHITE)
    # dome: half-ellipse sitting on the pediment, kept inside the art box
    d.pieslice([cx - 46, base - 94, cx + 46, base - 60], 180, 360,
               fill=WHITE)
    d.rectangle([cx - 5, base - 98, cx + 5, base - 92], fill=WHITE)
    d.ellipse([cx - 4, base - 101, cx + 4, base - 95], fill=WHITE)
    # amber base line
    d.rectangle([x0, base - 6, x1, base], fill=(242, 165, 65))
    # stars
    for sx, sy in ((x0 + 26, y0 + 22), (x1 - 30, y0 + 34), (x0 + 60, y0 + 52)):
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=AMBER)


def art_scales(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(220, 233, 245))
    cx = (x0 + x1) // 2
    base = y1 - 8
    # post, beam, base
    d.line([cx, y0 + 14, cx, base - 6], fill=INK, width=5)
    d.line([cx - 62, y0 + 26, cx + 62, y0 + 26], fill=INK, width=5)
    d.ellipse([cx - 5, y0 + 8, cx + 5, y0 + 18], fill=AMBER)
    d.rectangle([cx - 34, base - 6, cx + 34, base], fill=INK)
    for side in (-1, 1):
        px = cx + side * 62
        d.line([px, y0 + 26, px, y0 + 58], fill=INK, width=3)
        d.polygon([(px - 26, y0 + 58), (px + 26, y0 + 58), (px, y0 + 82)],
                  outline=INK, width=3, fill=(242, 165, 65))


def art_tents(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 217, 168))
    d.ellipse([x1 - 52, y0 + 10, x1 - 20, y0 + 42], fill=(242, 165, 65))
    base = y1
    d.rectangle([x0, base - 16, x1, base], fill=(196, 164, 110))
    for i, (tx, tw, th, col) in enumerate((
            (x0 + 18, 74, 52, (192, 57, 43)),
            (x0 + 108, 88, 62, (255, 255, 255)),
            (x0 + 214, 74, 52, (46, 95, 163)))):
        d.polygon([(tx, base - 16), (tx + tw // 2, base - 16 - th),
                   (tx + tw, base - 16)], fill=col, outline=INK, width=2)
        d.line([tx + tw // 2, base - 16 - th, tx + tw // 2, base - 16],
               fill=INK, width=2)


def art_bridge(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(191, 217, 232))
    deck_y = y0 + (y1 - y0) * 7 // 12
    # arch
    d.arc([x0 + 8, y0 + 6, x1 - 8, deck_y + 40], 180, 360, fill=INK, width=6)
    # suspenders
    for i in range(7):
        sx = x0 + 30 + i * ((x1 - x0 - 60) // 6)
        import math
        # height of arc at sx (ellipse approx)
        rx = (x1 - x0 - 16) / 2
        cx = (x0 + x1) / 2
        ry = (deck_y + 40 - (y0 + 6)) / 2
        cy = (y0 + 6 + deck_y + 40) / 2
        t = (sx - cx) / rx
        if abs(t) < 1:
            ay = cy - ry * math.sqrt(1 - t * t)
            d.line([sx, ay, sx, deck_y], fill=INK, width=2)
    # deck + towers
    d.rectangle([x0, deck_y, x1, deck_y + 8], fill=INK)
    for tx in (x0 + 26, x1 - 34):
        d.rectangle([tx, y0 + 22, tx + 8, deck_y], fill=INK)
    # water: two rows, kept strictly inside the art box
    for wy in (deck_y + 14, deck_y + 26):
        if wy + 10 > y1:
            break
        for k in range(6):
            wx = x0 + 8 + k * 52
            d.arc([wx, wy, wx + 34, wy + 10], 0, 180, fill=BLUE, width=3)


def art_chart(d, x0, y0, x1, y1):
    """Rising bars + arrow for the lead panel."""
    base = y1 - 6
    heights = [58, 92, 128, 164, 204]
    bw, gap = 46, 14
    total = len(heights) * bw + (len(heights) - 1) * gap
    sx = x0 + (x1 - x0 - total) // 2
    shades = [(46, 95, 163), (14, 124, 123), (14, 124, 123),
              (242, 165, 65), (228, 87, 46)]
    tops = []
    for i, hgt in enumerate(heights):
        bx = sx + i * (bw + gap)
        d.rectangle([bx, base - hgt, bx + bw, base], fill=shades[i],
                    outline=INK, width=2)
        tops.append((bx + bw // 2, base - hgt))
    d.line([x0, base, x1, base], fill=INK, width=3)
    # arrow along the tops
    pts = [(tops[0][0] - 18, tops[0][1] + 16)] + tops
    d.line(pts, fill=INK, width=4, joint="curve")
    hx, hy = tops[-1]
    d.polygon([(hx - 4, hy - 16), (hx + 18, hy - 2), (hx - 2, hy + 10)],
              fill=INK)
    d.text((x0 + 6, y0 + 2), "$83", font=font(SANS_B, 44), fill=CORAL)
    d.text((x0 + 8, y0 + 52), "NASDAQ: ANT", font=font(SANS_B, 17), fill=INK)


def main():
    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 116], fill=INK)
    d.text((32, 18), "19 NOVEMBER 2026", font=font(SERIF_B, 56), fill=WHITE)
    d.text((32, 82), "THURSDAY  •  THE WORLD IN ONE IMAGE",
           font=font(SANS_B, 20), fill=AMBER)
    d.text((W - 32, 30), "WORLD NEWS", font=font(SANS_B, 26),
           fill=WHITE, anchor="ra")
    d.line([W - 32 - 190, 66, W - 32, 66], fill=AMBER, width=3)
    d.text((W - 32, 76), "19 NOV 2026", font=font(SANS_B, 18),
           fill=AMBER, anchor="ra")

    # ---- lead: Anthropic IPO ----
    lx0, ly0, lx1, ly1 = 24, 128, 1000, 392
    panel(d, lx0, ly0, lx1, ly1)
    d.text((48, 146), "BUSINESS  •  MARKETS", font=font(SANS_B, 19),
           fill=TEAL)
    ty = 176
    ty = draw_text_block(d, 48, ty, ["ANTHROPIC DEBUTS", "ON NASDAQ"],
                         font(SANS_B, 46), INK, leading=52)
    ty += 8
    draw_text_block(
        d, 48, ty,
        ["$81.3bn listing at $83 a share —",
         "the biggest IPO in history."],
        font(SANS, 21), GREY, leading=28)
    art_chart(d, 668, 150, 976, 380)

    # ---- row 2: GTA VI / Jeffries ----
    story_panel(d, 24, 404, 502, 640,
                "CULTURE  •  GAMES", CORAL,
                "GTA VI ROLLS OUT WORLDWIDE",
                "After 13 years, gamers return to Vice City.",
                art_gta)
    story_panel(d, 522, 404, 1000, 640,
                "POLITICS  •  USA", BLUE,
                "JEFFRIES IN LINE TO BE SPEAKER",
                "Democrats nominate him — first Black Speaker.",
                art_capitol)

    # ---- row 3: ICJ / Gaza / Crimea ----
    story_panel(d, 24, 652, 352, 884,
                "LAW  •  THE HAGUE", BLUE,
                "WORLD COURT RULES ON MYANMAR",
                "Rohingya genocide case decided today.",
                art_scales, headline_size=24, sub_size=15, art_frac=0.40)
    story_panel(d, 368, 652, 696, 884,
                "CONFLICT  •  GAZA", RED,
                "ISRAEL LAUNCHES GAZA GROUND OP",
                "Troops enter central Gaza; families flee.",
                art_tents, headline_size=24, sub_size=15, art_frac=0.40)
    story_panel(d, 712, 652, 1000, 884,
                "WAR  •  UKRAINE", TEAL,
                "CRIMEA BRIDGE HIT AGAIN",
                "Traffic halted after a new strike.",
                art_bridge, headline_size=24, sub_size=15, art_frac=0.40)

    # ---- ticker (auto-fit to one line) ----
    d.rectangle([0, 896, W, 940], fill=INK)
    ticker = ("Cyclone Akvan nears India's east coast   •   Trump, Xi & Putin "
              "meet in Shenzhen   •   Voyager 1 reaches one light-day")
    tsize = 18
    while (d.textlength(ticker, font=font(SANS_B, tsize)) > 1000
           and tsize > 12):
        tsize -= 1
    d.text((512, 940 - (940 - 896 - tsize) // 2 - tsize), ticker,
           font=font(SANS_B, tsize), fill=AMBER, anchor="ma")

    # ---- footer ----
    d.text((512, 956),
           "Sources: BBC  •  Reuters  •  AP  •  Al Jazeera  •  Bloomberg",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    d.text((512, 980), "All events of 19 November 2026",
           font=font(SANS, 14), fill=GREY, anchor="ma")

    # ---- frame ----
    d.rectangle([5, 5, W - 6, H - 6], outline=INK, width=5)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
