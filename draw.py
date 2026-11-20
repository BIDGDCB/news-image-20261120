#!/usr/bin/env python3
"""Draw entry.png: a 1024x1024 summary of the world news of 20 November 2026.

Original design, drawn with Pillow shapes and DejaVu Sans. No photos, no
copied artwork. Deterministic: same input, same bytes. Run: python3 draw.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

# palette: deep ink-blue night, warm gold accents
INK_TOP = (8, 24, 46)
INK_BOT = (14, 38, 70)
PANEL = (20, 48, 88)
PANEL_LT = (26, 58, 104)
GOLD = (233, 178, 62)
WHITE = (244, 246, 249)
SOFT = (176, 194, 218)
FAINT = (120, 148, 180)
RULE = (52, 88, 140)
TEAL = (74, 196, 182)
RED = (226, 82, 82)
ORANGE = (233, 128, 60)
SKY = (96, 158, 230)
GREEN = (98, 198, 122)


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap into lines no wider than max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, lines, font, fill, lead=4):
    """Draw lines top-down; return y just below the last line."""
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + lead
    return y


def burst(d, cx, cy, r, fill):
    """A many-pointed starburst (explosion flash)."""
    pts = []
    for i in range(24):
        rad = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + i * 15)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=fill)


def globe_mark(d, cx, cy, r, color):
    """Simple line-art globe: circle, meridians, equator."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=4)
    d.ellipse((cx - int(r * 0.52), cy - r, cx + int(r * 0.52), cy + r),
              outline=color, width=3)
    d.line((cx - r, cy, cx + r, cy), fill=color, width=3)
    d.arc((cx - r, cy - int(r * 0.52), cx + r, cy + int(r * 0.52)),
          180, 360, fill=color, width=3)


def tile(d, x, y, w, h, kicker, title, body, accent):
    """One story card: coloured top strip, kicker, headline, body."""
    d.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=PANEL_LT)
    d.rounded_rectangle((x, y, x + w, y + 9), radius=4, fill=accent)
    d.text((x + 22, y + 22), kicker, font=fnt(BOLD, 19), fill=accent)
    yy = para(d, x + 22, y + 50,
              wrap(d, title, fnt(BOLD, 26), w - 44), fnt(BOLD, 26), WHITE, 2)
    para(d, x + 22, yy + 8,
         wrap(d, body, fnt(REG, 19), w - 44), fnt(REG, 19), SOFT, 3)


def main():
    img = Image.new("RGB", (W, H), INK_TOP)
    d = ImageDraw.Draw(img, "RGBA")

    # night-sky gradient
    for yy in range(H):
        t = yy / H
        col = tuple(int(INK_TOP[i] + (INK_BOT[i] - INK_TOP[i]) * t)
                    for i in range(3))
        d.line((0, yy, W, yy), fill=col)
    # faint star dots
    for gx in range(24, W, 52):
        for gy in range(24, H, 52):
            d.ellipse((gx, gy, gx + 2, gy + 2), fill=(255, 255, 255, 16))

    # ---------------- header ----------------
    d.text((36, 28), "THE WORLD IN ONE IMAGE", font=fnt(BOLD, 24), fill=GOLD)
    d.text((36, 58), "20 NOVEMBER 2026", font=fnt(BOLD, 60), fill=WHITE)
    d.text((36, 126), "Friday  \u00b7  Six stories that shaped the day",
           font=fnt(REG, 23), fill=SOFT)
    globe_mark(d, 946, 76, 44, GOLD)
    d.line((36, 166, 988, 166), fill=GOLD, width=4)

    # ---------------- hero: Ukraine strike ----------------
    hx, hy, hw, hh = 36, 186, 952, 200
    d.rounded_rectangle((hx, hy, hx + hw, hy + hh), radius=18, fill=PANEL)
    d.rectangle((hx, hy, hx + 10, hy + hh), fill=RED)
    burst(d, hx + hw - 92, hy + 100, 58, (226, 82, 82, 70))
    burst(d, hx + hw - 92, hy + 100, 34, RED)
    d.text((hx + 30, hy + 16), "TOP STORY  \u00b7  KYIV, UKRAINE",
           font=fnt(BOLD, 22), fill=RED)
    d.text((hx + 30, hy + 48), "RUSSIA'S MASSIVE STRIKE",
           font=fnt(BOLD, 42), fill=WHITE)
    d.text((hx + 30, hy + 98), "HOURS AFTER THE SUMMIT",
           font=fnt(BOLD, 42), fill=WHITE)
    para(d, hx + 30, hy + 152,
         wrap(d, "Moscow fires 100+ missiles and ~400 drones at Ukraine "
                 "overnight. Three Kyiv bridges hit; power grid "
                 "\u201cextremely critical\u201d.",
              fnt(REG, 19), hw - 240), fnt(REG, 19), SOFT, 3)

    # ---------------- 2 x 2 story grid ----------------
    gy, gh = 402, 224
    gw = 469
    gap = 14
    tile(d, 36, gy, gw, gh, "DIPLOMACY  \u00b7  SHENZHEN",
         "A \u2018PEACE DECLARATION\u2019 \u2014 NO BREAKTHROUGH",
         "Trump, Xi and Putin hail a joint declaration after their "
         "first three-way summit. Trump tells European leaders a "
         "\u201ctired\u201d Putin is ready for a deal.",
         GOLD)
    tile(d, 36 + gw + gap, gy, gw, gh, "MARKETS  \u00b7  NEW YORK",
         "AI STOCKS KEEP SLIDING",
         "US shares fall and Asian markets plunge on AI bubble fears "
         "\u2014 even after Anthropic's record $81bn debut closed 17% up.",
         SKY)
    tile(d, 36, gy + gh + gap, gw, gh, "MIDDLE EAST  \u00b7  THE GULF",
         "IRAN WAR COST PUT AT $48.3BN",
         "The Pentagon says the US war has cost $48.3bn so far, not "
         "counting damage to bases. The Senate blocks a bid to end it.",
         ORANGE)
    tile(d, 36 + gw + gap, gy + gh + gap, gw, gh, "CLIMATE  \u00b7  ANTALYA",
         "COP31 REACHES ITS FINAL DAY",
         "Climate talks close in T\u00fcrkiye today. Africa seeks tripled "
         "climate finance; Europe urges focus on existing pledges.",
         GREEN)

    # ---------------- also today strip ----------------
    ax, ay, aw, ah = 36, 880, 952, 66
    d.rounded_rectangle((ax, ay, ax + aw, ay + ah), radius=14, fill=(16, 40, 76))
    d.text((ax + 22, ay + 20), "ALSO TODAY", font=fnt(BOLD, 20), fill=TEAL)
    items = [
        "UK and EU agree a youth mobility scheme",
        "Poland probes mystery objects near its border",
        "Houthis claim strikes on Saudi targets",
    ]
    col_w = 258
    for i, it in enumerate(items):
        cx = ax + 178 + i * (col_w + 12)
        d.ellipse((cx, ay + 27, cx + 8, ay + 35), fill=GOLD)
        para(d, cx + 16, ay + 20,
             wrap(d, it, fnt(REG, 18), col_w - 20), fnt(REG, 18), WHITE, 2)
        if i < len(items) - 1:
            d.line((cx + col_w + 2, ay + 14, cx + col_w + 2, ay + ah - 14),
                   fill=RULE, width=2)

    # ---------------- footer ----------------
    d.line((36, 964, 988, 964), fill=RULE, width=2)
    d.text((36, 978), "Sources: BBC \u00b7 Reuters \u00b7 AP \u00b7 CNN \u00b7 Wall Street Journal",
           font=fnt(REG, 18), fill=FAINT)
    d.text((792, 978), "20 NOVEMBER 2026", font=fnt(BOLD, 18), fill=GOLD)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
