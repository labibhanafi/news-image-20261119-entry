#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' — a one-page newspaper for Thursday 19 November 2026.

Pure deterministic drawing with Pillow: no randomness, no network, no photos.
Running this file writes entry.png (1024x1024) next to itself, and prints
the bottom edge of the text columns so layout overflow is visible.
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 20
CONTENT_W = W - 2 * MARGIN

PAPER = "#f7f3e8"
INK = "#14181d"
RED = "#b3202c"
NAVY = "#16324f"
GOLD = "#c9a227"
LIGHT = "#ddd5bd"
SKY = "#dfe7ec"
CYAN = "#2e7f9e"
PINK = "#c94f7c"

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w, measured with textlength."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; return the y just below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
HERO = {
    "kicker": "SHENZHEN \u00b7 APEC SUMMIT",
    "headline": "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
    "standfirst": (
        "The first trilateral of the three leaders. Nuclear arms top the "
        "agenda \u2014 the last US\u2013Russia pact expired in February \u2014 with "
        "Ukraine and Iran in the room. No agreement is expected."
    ),
}

PICTURED = [
    {
        "kind": "gta",
        "kicker": "GAMING \u00b7 LAUNCH DAY",
        "headline": "GTA VI IS HERE AT LAST",
        "sub": (
            "A 13-year wait ends as the game launches worldwide on PS5 and "
            "Xbox. First reviews score it 99 out of 100, pre-orders passed "
            "$1.5 billion, and 2.3 million people watched live streams in "
            "the first hours."
        ),
    },
    {
        "kind": "chart",
        "kicker": "MARKETS",
        "headline": "ANTHROPIC RAISES $81.3BN IN THE BIGGEST IPO OF ALL TIME",
        "sub": (
            "The AI company's market debut smashes every record for an "
            "initial public offering."
        ),
    },
]

SMALL = [
    {
        "kind": "court",
        "kicker": "THE HAGUE \u00b7 JUSTICE",
        "headline": "ROHINGYA VERDICT DAY AT THE WORLD COURT",
        "sub": "The ICJ delivers its judgment in the genocide case against Myanmar, seven years on.",
    },
    {
        "kind": "cyclone",
        "kicker": "BAY OF BENGAL \u00b7 WEATHER",
        "headline": "CYCLONE AKVAN BEARS DOWN ON ODISHA",
        "sub": "Schools shut and the railways lead preparations as the severe storm nears India's east coast.",
    },
    {
        "kind": "bridge",
        "kicker": "CRIMEA \u00b7 EUROPE",
        "headline": "CRIMEA BRIDGE CLOSED AFTER NEW ATTACK",
        "sub": "Traffic over the Kerch Strait halted at midnight; officials say the damage is still being assessed.",
    },
    {
        "kind": "probe",
        "kicker": "DEEP SPACE \u00b7 SCIENCE",
        "headline": "VOYAGER 1 CROSSES ONE LIGHT-DAY FROM HOME",
        "sub": "NASA's farthest spacecraft reaches a new frontier, nearly 50 years after launch.",
    },
]

TEXT_STORIES = [
    ("WASHINGTON \u00b7 US POLITICS", "Jeffries to be first Black Speaker of the House",
     "House Democrats nominate Hakeem Jeffries after their midterm wave."),
    ("WASHINGTON \u00b7 COURTS", "Trump's third Supreme Court bid to end Venezuelan migrant protections",
     "The administration asks the justices again to lift the shield."),
    ("CARACAS \u00b7 AMERICAS", "US and Venezuela restore military ties",
     "Training and intelligence cooperation resume, says Defence Secretary Hegseth."),
    ("MIAMI \u00b7 AMERICAS", "Pastor convicted over 2021 assassination of Haiti's president",
     "A Miami court finds the US-Haitian pastor guilty in the Mo\u00efse plot."),
    ("PANAMA \u00b7 AMERICAS", "Second arrest over attack on journalist's home",
     "Prosecutors move in the Rolando Rodr\u00edguez case."),
    ("HORMUZ \u00b7 MIDDLE EAST", "Tanker struck off Khasab; crew safe",
     "UKMTO reports an engine-room strike six nautical miles north of Khasab."),
    ("RIYADH \u00b7 MIDDLE EAST", "Houthis target Riyadh; kingdom later gives all-clear",
     "Civil Defence warned the capital, then stood the alert down."),
    ("SANCTIONS \u00b7 MIDDLE EAST", "US sanctions Hezbollah-linked network",
     "Three people and three entities join the OFAC list."),
    ("GAZA \u00b7 MIDDLE EAST", "Four nations demand aid reach flooded Gaza",
     "Australia, Canada, Italy and the UK call for immediate, unrestricted access."),
    ("JERUSALEM \u00b7 ISRAEL", "Herzog asks Eisenkot to form a government",
     "The president turns to the former army chief, bypassing Netanyahu."),
    ("TOKYO \u00b7 ASIA", "India and Japan open 2+2 defence talks",
     "Singh and Jaishankar in Tokyo as defence and security ties deepen."),
    ("NORTH KOREA \u00b7 ASIA", "IAEA: North Korea expanding uranium enrichment",
     "Inspectors report growth at the North's nuclear facilities."),
    ("MANILA \u00b7 ASIA", "US and Philippines pursue $2bn-plus loan package",
     "The White House says the two allies will pursue the financing."),
    ("DELHI \u00b7 INDIA", "Delhi schools reopen as pollution curbs lift",
     "Classes resume in person after GRAP Stage-III restrictions end."),
    ("NAIROBI \u00b7 AFRICA", "Kenya's milk shortage deepens in drought",
     "Farmers struggle and prices climb as the dry spell bites."),
    ("SOCIETY \u00b7 DATA", "Islam on track to be world's largest faith by 2035",
     "A new Pew projection puts it ahead of Christianity within a decade."),
    ("OIL \u00b7 MARKETS", "Oil prices fall as supply improves",
     "Better flows outweigh Middle East tension, traders say."),
    ("NEW YORK \u00b7 CULTURE", "Van Gogh record: $190.4m for Blossoming Chestnut Trees",
     "The Sotheby's sale sets the artist's auction record after a Nazi-era claim was settled."),
    ("WELLINGTON \u00b7 SPORT", "India open first Test against New Zealand",
     "The series gets under way in Wellington."),
    ("BADMINTON \u00b7 SPORT", "Sindhu back in the world top five",
     "Lakshya Sen joins her in the men's top ten."),
]

BRIEFS = [
    "Canada sanctions Israeli settlers over West Bank expansion",
    "Musk calls his midterm spending 'pretty foolish'",
    "World COPD Day marked across the globe",
    "Vaishali wins by forfeit at Total Chess",
    "Paraguay extends Ueno Bank guarantee deadline to 2 December",
]

NUMBERS = [
    "$81.3bn \u2014 biggest IPO ever",
    "$190.4m \u2014 Van Gogh record",
    "1 light-day \u2014 Voyager 1",
    "99/100 \u2014 GTA VI first reviews",
    "$1.5bn \u2014 GTA VI pre-orders",
]

TOTAL_STORIES = 1 + len(PICTURED) + len(SMALL) + len(TEXT_STORIES) + len(BRIEFS)


# ------------------------------------------------------------ illustrations
def hero_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    draw.ellipse([x + w - 50, y + 8, x + w - 18, y + 40], fill=GOLD)
    # three flags flying in the sky, top left
    for i, fx in enumerate((12, 62, 112)):
        px = x + fx
        draw.line([px, y + 8, px, y + 42], fill=INK, width=2)
        fw, fh, top = 36, 20, y + 8
        if i == 0:  # United States: stripes + blue canton
            for s in range(5):
                col = RED if s % 2 == 0 else "#ffffff"
                draw.rectangle([px + 2, top + s * 4, px + 2 + fw, top + s * 4 + 4], fill=col)
            draw.rectangle([px + 2, top, px + 17, top + 10], fill=NAVY)
        elif i == 1:  # China: red field, gold stars
            draw.rectangle([px + 2, top, px + 2 + fw, top + fh], fill=RED)
            draw.ellipse([px + 6, top + 3, px + 12, top + 9], fill=GOLD)
            draw.ellipse([px + 15, top + 2, px + 18, top + 5], fill=GOLD)
            draw.ellipse([px + 16, top + 7, px + 19, top + 10], fill=GOLD)
            draw.ellipse([px + 15, top + 12, px + 18, top + 15], fill=GOLD)
        else:  # Russia: white / blue / red
            draw.rectangle([px + 2, top, px + 2 + fw, top + 7], fill="#ffffff")
            draw.rectangle([px + 2, top + 7, px + 2 + fw, top + 13], fill=NAVY)
            draw.rectangle([px + 2, top + 13, px + 2 + fw, top + fh], fill=RED)
        draw.rectangle([px + 2, top, px + 2 + fw, top + fh], outline=INK, width=1)
    # Shenzhen skyline along the bottom
    towers = [(6, 40, 26), (36, 26, 22), (62, 50, 30), (96, 32, 20),
              (120, 58, 26), (150, 38, 22), (176, 48, 28), (208, 28, 20),
              (232, 42, 24), (260, 34, 20)]
    for dx, th, tw in towers:
        if dx + tw > w - 4:
            continue
        draw.rectangle([x + dx, y + h - th, x + dx + tw, y + h - 5], fill=NAVY)
        for wy in range(y + h - th + 5, y + h - 11, 9):
            draw.rectangle([x + dx + 4, wy, x + dx + 8, wy + 3], fill=GOLD)
            draw.rectangle([x + dx + tw - 8, wy, x + dx + tw - 4, wy + 3], fill=GOLD)
    draw.rectangle([x, y + h - 5, x + w, y + h], fill=INK)


def gta_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY, outline=INK, width=2)
    for i, (dx, bh, bw) in enumerate([(6, 58, 17), (28, 80, 20), (53, 48, 15),
                                      (73, 68, 18), (96, 52, 15)]):
        if dx + bw > w - 34:
            continue
        col = CYAN if i % 2 == 0 else PINK
        draw.rectangle([x + dx, y + h - bh, x + dx + bw, y + h - 4], outline=col, width=2)
        for wy in range(y + h - bh + 7, y + h - 12, 11):
            draw.line([x + dx + 3, wy, x + dx + bw - 3, wy], fill=GOLD, width=2)
    for px in (x + w - 24, x + w - 48):
        draw.line([px, y + h - 4, px + 4, y + 26], fill=GOLD, width=3)
        for ang in (-38, -14, 12, 36):
            ex = px + 4 + int(15 * math.cos(math.radians(ang - 90)))
            ey = y + 26 + int(11 * math.sin(math.radians(ang - 90))) + 6
            draw.line([px + 4, y + 26, ex, ey], fill=GOLD, width=2)
    draw.ellipse([x + w - 24, y + 6, x + w - 9, y + 21], fill=PINK)


def chart_art(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill="#ffffff", outline=INK, width=2)
    base = y + h - 12
    draw.line([x + 10, y + 8, x + 10, base], fill=INK, width=2)
    draw.line([x + 10, base, x + w - 8, base], fill=INK, width=2)
    for i, bh in enumerate((14, 22, 18, 30, 42, 56)):
        bx = x + 15 + i * 18
        if bx + 10 > x + w - 8:
            break
        draw.rectangle([bx, base - bh, bx + 10, base], fill=NAVY)
    pts = [(x + 17, base - 12), (x + 38, base - 24), (x + 59, base - 20),
           (x + 80, base - 40), (x + 101, base - 52), (x + w - 13, base - 68)]
    draw.line(pts, fill=RED, width=3)
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD, outline=INK)


def small_art(draw, kind, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=1)
    cx = x + w // 2
    cy = y + h // 2
    if kind == "court":
        draw.polygon([(cx - 40, y + 13), (cx + 40, y + 13), (cx, y + 2)], fill=NAVY)
        draw.rectangle([cx - 42, y + 14, cx + 42, y + 17], fill=NAVY)
        for i in range(5):
            px = cx - 32 + i * 16
            draw.rectangle([px - 2, y + 19, px + 2, y + h - 7], fill=NAVY)
        draw.rectangle([cx - 42, y + h - 6, cx + 42, y + h - 3], fill=NAVY)
    elif kind == "cyclone":
        for rx, ry in ((30, 13), (20, 9), (11, 5)):
            draw.arc([cx - rx, cy - ry, cx + rx, cy + ry], start=15, end=330,
                     fill=NAVY, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        draw.line([x + 14, cy + 9, x + 44, cy + 9], fill=CYAN, width=2)
        draw.line([x + w - 44, cy - 9, x + w - 14, cy - 9], fill=CYAN, width=2)
    elif kind == "bridge":
        draw.line([x + 8, y + h - 7, x + w - 8, y + h - 7], fill=INK, width=3)
        for tx in (cx - 34, cx + 34):
            draw.rectangle([tx - 3, y + 6, tx + 3, y + h - 7], fill=NAVY)
        draw.arc([cx - 34, y - 8, cx + 34, y + 26], start=180, end=360, fill=RED, width=2)
        for hx in range(cx - 28, cx + 29, 14):
            draw.line([hx, y + 12, hx, y + h - 7], fill=RED, width=1)
        draw.rectangle([x + 16, y + h - 13, x + 40, y + h - 9], fill=RED)
        draw.rectangle([x + w - 40, y + h - 13, x + w - 16, y + h - 9], fill=RED)
    else:  # probe
        draw.rectangle([cx - 7, cy - 6, cx + 7, cy + 6], fill=GOLD, outline=INK)
        draw.rectangle([cx - 36, cy - 4, cx - 9, cy + 4], fill=NAVY)
        draw.rectangle([cx + 9, cy - 4, cx + 36, cy + 4], fill=NAVY)
        draw.line([cx + 3, cy - 5, cx + 15, y + 6], fill=INK, width=2)
        draw.arc([cx + 9, y + 2, cx + 27, y + 16], start=250, end=80, fill=RED, width=2)
        for sx, sy in ((x + 16, y + 6), (x + w - 18, y + 8), (x + 28, y + h - 8),
                       (x + w - 34, y + h - 7)):
            draw.ellipse([sx, sy, sx + 3, sy + 3], fill=INK)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    f_title = font(SERIF_B, 42)
    f_date = font(SANS_B, 15)
    f_sub = font(SANS_B, 12)
    f_kicker = font(SANS_B, 11)
    f_kicker_s = font(SANS_B, 8)
    f_hero_head = font(SERIF_B, 29)
    f_stand = font(SANS, 12)
    f_pic_head = font(SERIF_B, 22)
    f_pic_sub = font(SANS, 11)
    f_small_head = font(SERIF_B, 15)
    f_small_sub = font(SANS, 9)
    f_story_head = font(SANS_B, 16)
    f_story_sub = font(SANS, 9)
    f_brief = font(SANS, 10)
    f_num = font(SANS_B, 10)
    f_foot = font(SANS, 9)

    # masthead
    centered(draw, 6, "THE WORLD IN ONE DAY", f_title, INK)
    draw.line([MARGIN, 54, W - MARGIN, 54], fill=RED, width=3)
    centered(draw, 59, "THURSDAY \u00b7 19 NOVEMBER 2026", f_date, RED)
    centered(draw, 80, f"{TOTAL_STORIES} STORIES \u00b7 FIVE CONTINENTS \u00b7 ONE DAY",
             f_sub, NAVY)
    draw.line([MARGIN, 98, W - MARGIN, 98], fill=INK, width=2)
    draw.line([MARGIN, 102, W - MARGIN, 102], fill=INK, width=1)

    # hero: art left, words right
    hy = 110
    hero_art(draw, MARGIN, hy, 292, 118)
    tx = MARGIN + 306
    tw = W - MARGIN - tx
    y = hy + 2
    draw.text((tx, y), HERO["kicker"], font=f_kicker, fill=RED)
    y += 16
    y = block(draw, tx, y, HERO["headline"], f_hero_head, INK, tw, 32)
    y += 2
    block(draw, tx, y, HERO["standfirst"], f_stand, INK, tw, 15)
    draw.line([MARGIN, 236, W - MARGIN, 236], fill=INK, width=1)

    # pictured pair: art left inside each column, words right
    py = 244
    col_w = (CONTENT_W - 14) // 2
    for i, story in enumerate(PICTURED):
        cx0 = MARGIN + i * (col_w + 14)
        if story["kind"] == "gta":
            gta_art(draw, cx0, py, 132, 124)
        else:
            chart_art(draw, cx0, py, 132, 124)
        wx = cx0 + 142
        ww = col_w - 142
        y = py + 2
        draw.text((wx, y), story["kicker"], font=f_kicker, fill=RED)
        y += 16
        y = block(draw, wx, y, story["headline"], f_pic_head, INK, ww, 24)
        y += 2
        block(draw, wx, y, story["sub"], f_pic_sub, INK, ww, 13)
        if i == 0:
            draw.line([cx0 + col_w + 7, py, cx0 + col_w + 7, py + 124],
                      fill=INK, width=1)
    draw.line([MARGIN, 376, W - MARGIN, 376], fill=INK, width=1)

    # small pictured row: four columns
    sy = 384
    scol_w = (CONTENT_W - 3 * 10) // 4
    for i, story in enumerate(SMALL):
        cx0 = MARGIN + i * (scol_w + 10)
        small_art(draw, story["kind"], cx0, sy, scol_w, 32)
        y = sy + 36
        draw.text((cx0, y), story["kicker"], font=f_kicker_s, fill=RED)
        y += 11
        y = block(draw, cx0, y, story["headline"], f_small_head, INK, scol_w, 17)
        y += 1
        block(draw, cx0, y, story["sub"], f_small_sub, INK, scol_w, 11)
    draw.line([MARGIN, 502, W - MARGIN, 502], fill=INK, width=1)

    # text stories: three columns, filled in order and balanced by height
    ty = 512
    tcol_w = (CONTENT_W - 2 * 12) // 3

    def story_height(story):
        _, head, sub = story
        hh = len(wrap(draw, head, f_story_head, tcol_w)) * 16
        sh = len(wrap(draw, sub, f_story_sub, tcol_w)) * 11
        return 10 + hh + sh + 4

    heights = [story_height(s) for s in TEXT_STORIES]
    target = sum(heights) / 3.0
    columns, cur, acc = [], [], 0.0
    for story, hh in zip(TEXT_STORIES, heights):
        if cur and acc + hh > target and len(columns) < 2:
            columns.append(cur)
            cur, acc = [], 0.0
        cur.append(story)
        acc += hh
    columns.append(cur)

    bottom = ty
    for ci, col in enumerate(columns):
        cx0 = MARGIN + ci * (tcol_w + 12)
        y = ty
        for kicker, head, sub in col:
            draw.text((cx0, y), kicker, font=f_kicker_s, fill=RED)
            y += 10
            y = block(draw, cx0, y, head, f_story_head, INK, tcol_w, 16)
            y = block(draw, cx0, y, sub, f_story_sub, INK, tcol_w, 11)
            y += 4
            draw.line([cx0, y - 2, cx0 + tcol_w, y - 2], fill=LIGHT, width=1)
        bottom = max(bottom, y)
        if ci < 2:
            draw.line([cx0 + tcol_w + 6, ty, cx0 + tcol_w + 6, bottom],
                      fill=INK, width=1)
    print(f"text columns bottom = {bottom} (brief strip at 954)")

    # world in brief strip
    by = 954
    draw.rectangle([MARGIN, by, W - MARGIN, by + 30], fill=NAVY)
    brief_text = "WORLD IN BRIEF:  " + "  \u00b7  ".join(BRIEFS)
    yy = by + 4
    for line in wrap(draw, brief_text, f_brief, CONTENT_W - 16)[:2]:
        draw.text((MARGIN + 8, yy), line, font=f_brief, fill="#ffffff")
        yy += 12

    # by the numbers strip
    ny = 988
    draw.rectangle([MARGIN, ny, W - MARGIN, ny + 18], fill=GOLD)
    num_text = "BY THE NUMBERS:  " + "  \u00b7  ".join(NUMBERS)
    nw = draw.textlength(num_text, font=f_num)
    draw.text(((W - nw) / 2, ny + 4), num_text, font=f_num, fill=INK)

    # footer
    centered(draw, 1010,
             "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Al Jazeera \u00b7 Le Monde \u00b7 Yonhap "
             "\u00b7 NDTV \u00b7 Artnet \u00b7 UKMTO   |   Drawn and set by program \u2014 no photographs",
             f_foot, NAVY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} stories={TOTAL_STORIES}")


if __name__ == "__main__":
    main()
