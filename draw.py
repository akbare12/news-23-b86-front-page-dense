#!/usr/bin/env python3
"""news-23 b86 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. Run: python3 draw.py -> entry.png"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

BLACK = (10, 10, 10)
RED = (178, 0, 0)
DARKRED = (140, 0, 0)
NAVY = (12, 28, 74)
BLUE = (18, 72, 160)
GREEN = (11, 93, 46)
GOLD = (176, 128, 0)
GOLDL = (201, 162, 39)
TEAL = (0, 120, 120)
PURPLE = (110, 44, 150)
GRAY = (90, 90, 90)
LGRAY = (230, 230, 230)
CREAM = (250, 244, 224)

def tw(text, font, maxw):
    """Wrap text to fit maxw; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center(x, w, text, font):
    return x + (w - d.textlength(text, font=font)) / 2

def chip(x, y, text, fill):
    f = F(SANS_B, 10)
    w = d.textlength(text, font=f) + 12
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=fill)
    d.text((x + 6, y + 2), text, font=f, fill="white")
    return w

# ---------- masthead ----------
d.rectangle([0, 0, W, 50], fill=BLACK)
d.text((16, 4), "THE WORLD TODAY", font=F(SERIF_B, 40), fill="white")
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 16 - d.textlength(dt, font=F(SANS_B, 15)), 16), dt,
       font=F(SANS_B, 15), fill=GOLDL)

# ---------- kicker ----------
d.rectangle([0, 50, W, 70], fill=RED)
kick = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
d.text((center(0, W, kick, F(SANS_B, 13)), 54), kick, font=F(SANS_B, 13), fill="white")

# ---------- number strip (2 rows x 5) ----------
nums = [
    [("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLUE),
     ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", GOLD),
     ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE)],
    [("$450M", "SKUBAL DEAL", BLUE), ("165", "RUSSIAN MISSILES/WEEK", RED),
     ("12,000", "CLEARED IN MANCHESTER", GREEN), ("264 kg", "EXPLOSIVES SEIZED", GOLD),
     ("$107.3B", "ANTHROPIC IPO", PURPLE)],
]
for r, row in enumerate(nums):
    yv = 72 + r * 27
    for c, (val, lab, col) in enumerate(row):
        x = 16 + c * 200
        d.text((x, yv), val, font=F(SANS_B, 18), fill=col)
        d.text((x, yv + 19), lab, font=F(SANS_B, 8), fill=GRAY)

# ---------- region bar ----------
d.rectangle([0, 130, W, 148], fill=BLACK)
segs = [("ASIA-PACIFIC 7", 224, NAVY), ("AMERICAS 8", 256, RED),
        ("MIDDLE EAST 6", 192, GOLD), ("EUROPE 5", 160, TEAL),
        ("AFRICA 3", 96, PURPLE), ("WORLD 2", 64, (60, 60, 60))]
x = 16
for label, w, col in segs:
    d.rectangle([x, 130, x + w, 148], fill=col)
    d.text((center(x, w, label, F(SANS_B, 11)), 133), label, font=F(SANS_B, 11), fill="white")
    x += w

# ---------- THE DAY IN UTC ----------
utc = "THE DAY IN UTC    ~00:00 Kospi dives    ~06:30 Guterres opens    ~09:00 Power Index    ~12:00 Paris 2% tax    ~15:00 Kyiv missiles"
d.text((16, 151), utc, font=F(SANS, 10), fill=BLACK)
d.text((W - 16 - d.textlength("~ APPROX", font=F(SANS, 10)), 151), "~ APPROX",
       font=F(SANS, 10), fill=GRAY)

# ---------- hero scenes ----------
HX = [16, 352, 688]
HW = 320

# scene 1: Kospi skyline + chart
sx, sy = HX[0], 164
d.rectangle([sx, sy, sx + HW, sy + 98], fill=(8, 22, 54))
import random
random.seed(86)
for bx in range(sx + 8, sx + HW - 8, 26):
    bh = random.randint(28, 62)
    d.rectangle([bx, sy + 98 - bh - 16, bx + 20, sy + 98 - 16], fill=(16, 38, 84))
    for wy in range(sy + 98 - bh - 12, sy + 98 - 20, 9):
        for wx in (bx + 4, bx + 12):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
pts = [(sx + 10, sy + 62), (sx + 55, sy + 48), (sx + 100, sy + 58),
       (sx + 150, sy + 34), (sx + 200, sy + 44), (sx + 250, sy + 22),
       (sx + 305, sy + 14)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="white")
d.text((sx + 8, sy + 4), "-3.3%", font=F(SANS_B, 26), fill=(255, 80, 80))
d.rectangle([sx, sy + 98, sx + HW, sy + 114], fill=BLACK)
d.text((sx + 8, sy + 100), "KOSPI 4,708.54  \u00b7  -161 PTS", font=F(SANS_B, 11), fill="white")

# scene 2: Guterres globe
sx = HX[1]
d.rectangle([sx, sy, sx + HW, sy + 98], fill=GREEN)
d.text((sx + 10, sy + 6), "150 DELEGATES", font=F(SANS_B, 26), fill=(255, 214, 90))
d.text((sx + 10, sy + 34), "BACK A RISK", font=F(SANS_B, 26), fill=(255, 214, 90))
d.text((sx + 10, sy + 62), "FRAMEWORK", font=F(SANS_B, 26), fill=(255, 214, 90))
cx, cy, r = sx + 268, sy + 49, 40
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 224, 190))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(11, 93, 46), width=2)
d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(11, 93, 46), width=1)
d.line([cx - r, cy, cx + r, cy], fill=(11, 93, 46), width=1)
d.arc([cx - r, cy - 18, cx + r, cy + 18], 0, 360, fill=(11, 93, 46), width=1)
d.rectangle([sx, sy + 98, sx + HW, sy + 114], fill=BLACK)
d.text((sx + 8, sy + 100), "UN  \u00b7  BRIDGETOWN", font=F(SANS_B, 11), fill="white")

# scene 3: Power Index bars
sx = HX[2]
d.rectangle([sx, sy, sx + HW, sy + 98], fill=CREAM)
d.text((sx + 10, sy + 4), "NARROWEST SINCE 2018", font=F(SANS_B, 10), fill=BLACK)
d.text((sx + HW - 8 - d.textlength("GAP 5.3", font=F(SANS_B, 10)), sy + 4),
       "GAP 5.3", font=F(SANS_B, 10), fill=RED)
bars = [("US", 78.9, NAVY, sx + 30), ("CHINA", 73.6, RED, sx + 135),
        ("INDIA", 40.5, GOLD, sx + 240)]
base = sy + 96
for lab, val, col, bx in bars:
    bh = int(val / 78.9 * 52)
    d.rectangle([bx, base - bh, bx + 62, base], fill=col)
    d.text((center(bx, 62, f"{val}", F(SANS_B, 14)), base - bh - 18),
           f"{val}", font=F(SANS_B, 14), fill=BLACK)
    d.text((center(bx, 62, lab, F(SANS_B, 11)), base - 16),
           lab, font=F(SANS_B, 11), fill="white")
d.rectangle([sx, sy + 98, sx + HW, sy + 114], fill=BLACK)
d.text((sx + 8, sy + 100), "ASIA POWER INDEX 2026", font=F(SANS_B, 11), fill="white")

# ---------- hero headlines / bodies / source+chip ----------
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
for i, (head, body, src, ch) in enumerate(heroes):
    x = HX[i]
    hl = tw(head, F(SANS_B, 20), HW)
    yy = 286
    for ln in hl[:2]:
        d.text((x, yy), ln, font=F(SANS_B, 20), fill=BLACK)
        yy += 23
    bl = tw(body, F(SANS, 11), HW)
    yy = 330
    for ln in bl[:2]:
        d.text((x, yy), ln, font=F(SANS, 11), fill=BLACK)
        yy += 14
    d.text((x, 359), src, font=F(SANS, 9), fill=GRAY)
    cw = d.textlength(ch, font=F(SANS_B, 10)) + 12
    chip(x + HW - cw, 357, ch, BLUE)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 380, W, 398], fill=BLACK)
d.text((16, 383), "MORE OF THE DAY  \u2014  10 STORIES", font=F(SANS_B, 12), fill="white")

# ---------- 10 cards ----------
cards = [
    ("AMERICAS", "1", "BESSESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", NAVY),
    ("FBI", "2", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", (60, 60, 60)),
    ("WHITE HOUSE", "3", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", GOLD),
    ("MARKETS", "4", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", TEAL),
    ("SPORT", "5", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", RED),
    ("SPORT", "6", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", RED),
    ("LEGAL", "7", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", PURPLE),
    ("TECH", "8", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", BLUE),
    ("EUROPE", "9", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", GOLD),
    ("SPACE", "10", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", PURPLE),
]
CW, CG = 195, 5
for i, (cat, num, head, body, src, ch, col) in enumerate(cards):
    cx = 16 + (i % 5) * (CW + CG)
    cy = 404 + (i // 5) * 86
    d.rectangle([cx, cy, cx + CW, cy + 80], outline=(200, 200, 200), width=1)
    d.rectangle([cx, cy, cx + CW, cy + 15], fill=col)
    d.text((cx + 5, cy + 2), cat, font=F(SANS_B, 9), fill="white")
    d.text((cx + CW - 5 - d.textlength(num, font=F(SANS_B, 9)), cy + 2),
           num, font=F(SANS_B, 9), fill="white")
    hl = tw(head, F(SANS_B, 12), CW - 10)
    yy = cy + 19
    for ln in hl[:2]:
        d.text((cx + 5, yy), ln, font=F(SANS_B, 12), fill=BLACK)
        yy += 14
    d.text((cx + 5, cy + 50), body, font=F(SANS, 10), fill=BLACK)
    d.text((cx + 5, cy + 66), src, font=F(SANS, 9), fill=GRAY)
    cw = d.textlength(ch, font=F(SANS_B, 10)) + 12
    chip(cx + CW - cw - 4, cy + 64, ch, BLUE if ch == "REPORTED" else RED)

# ---------- WHERE IT HAPPENED / ALSO strip ----------
d.rectangle([0, 584, W, 602], fill=BLACK)
d.text((16, 587), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill="white")
d.text((340, 587), "ALSO ON MONDAY", font=F(SANS_B, 12), fill="white")

# ---------- map ----------
d.rectangle([16, 608, 330, 836], outline=BLACK, width=1)
d.polygon([(40, 622), (110, 612), (140, 652), (130, 730), (110, 800), (70, 812),
           (45, 762), (35, 690)], fill=(196, 224, 178))
d.polygon([(170, 622), (225, 612), (240, 662), (225, 732), (200, 802),
           (175, 772), (165, 692)], fill=(196, 224, 178))
d.polygon([(245, 622), (300, 612), (312, 662), (300, 732), (270, 782),
           (250, 732), (240, 672)], fill=(196, 224, 178))
d.polygon([(285, 800), (312, 800), (310, 826), (288, 826)], fill=(196, 224, 178))
pins = [(292, 644), (112, 782), (272, 667), (108, 667), (122, 644),
        (228, 680), (88, 700), (52, 717), (72, 747), (92, 766),
        (210, 657), (185, 640), (248, 630)]
for n, (px, py) in enumerate(pins, 1):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline="white", width=1)
    d.text((center(px, 0, str(n), F(SANS_B, 9)), py - 6), str(n),
           font=F(SANS_B, 9), fill="white")
d.text((24, 806), "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", font=F(SANS, 8), fill=BLACK)
d.text((24, 816), "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", font=F(SANS, 8), fill=BLACK)
d.text((24, 826), "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", font=F(SANS, 8), fill=BLACK)

# ---------- ALSO list ----------
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after pact rejected",
    "Benghazi: UN demands probe of port attacks",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Sudan: defences down drones",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
claims = {18, 25}
for i, item in enumerate(also):
    n = 14 + i
    yy = 612 + i * 12
    txt = f"{n}. {item}"
    if n in claims:
        txt += "  [CLAIM]"
        d.text((340, yy), txt, font=F(SANS, 11), fill=RED)
    else:
        d.text((340, yy), txt, font=F(SANS, 11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([16, 842, 1008, 910], outline=RED, width=2)
d.text((24, 848), "DATE CHECK", font=F(SANS_B, 13), fill=RED)
rh = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
d.text((1008 - 8 - d.textlength(rh, font=F(SANS_B, 9)), 851), rh,
       font=F(SANS_B, 9), fill=RED)
d.text((24, 868),
       "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU\u2013Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)",
       font=F(SANS, 11), fill=BLACK)
d.text((24, 888),
       "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
       font=F(SANS, 11), fill=BLACK)

# ---------- footer ----------
d.text((16, 918), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=F(SANS, 10), fill=GRAY)
d.text((16, 934), "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
       font=F(SANS, 10), fill=GRAY)
d.text((16, 950), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=F(SANS, 10), fill=GRAY)
d.line([16, 972, 1008, 972], fill=GOLDL, width=2)
foot = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text((center(0, W, foot, F(SANS_B, 13)), 982), foot, font=F(SANS_B, 13), fill=GOLD)

img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes")
