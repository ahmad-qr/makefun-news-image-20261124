#!/usr/bin/env python3
"""Build the 24 November 2026 world-news summary image (1024x1024).

Draws ten verified stories from Tuesday 24 November 2026 with Pillow.
Story sources: Kyiv Independent, NPR, AP, FT, AFP, EU, PBS, C54.
"""
from PIL import Image as PILImage, ImageDraw as PILDraw, ImageFont as PILFont

SIZE = (1024, 1024)
PAPER = (248, 246, 241)
DARK = (10, 30, 56)
ACCENT = (198, 160, 40)
TEXT = (20, 26, 34)
MUTED = (95, 101, 110)
ALT_ROW = (238, 236, 230)
RULE = (212, 208, 200)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CATEGORY_COLORS = {
    "WAR": (158, 32, 32),
    "TECH": (30, 80, 160),
    "MARKETS": (150, 110, 20),
    "CLIMATE": (176, 74, 28),
    "POLITICS": (24, 110, 88),
    "US": (30, 80, 160),
    "DISASTER": (120, 72, 160),
    "HEALTH": (24, 110, 88),
}

NEWS = [
    ("WAR", "Russian war death toll nears 700,000",
     "Leaked government data analysed by media puts deaths near 700,000. (Kyiv Independent)"),
    ("WAR", "Ukrainian drones 'hit Russian warship' off Libya",
     "Zelenskyy says drones struck the warship at a Libyan naval base. (NPR)"),
    ("WAR", "Poland scrambles jets as drone enters its airspace",
     "Air defences activated near Dorohusk during overnight strikes on Ukraine."),
    ("TECH", "Nvidia board reinstates Jensen Huang as CEO",
     "Board unanimously restores Huang after resignation and espionage probes. (AP)"),
    ("MARKETS", "Trump 'made up to $15m' on Nvidia shares",
     "FT reports Trump's gains after Huang's return to Nvidia. (FT)"),
    ("CLIMATE", "COP31 climate talks break down",
     "Negotiations in Turkiye collapse over fossil-fuel phase-out language. (AFP)"),
    ("POLITICS", "EU unveils 22nd sanctions package on Russia",
     "New measures target Moscow's war economy and sanctions evasion. (EU)"),
    ("US", "ICE arrests at Seattle airport spark outcry",
     "Father and daughter detained en route to a family baptism. (PBS)"),
    ("DISASTER", "Himalayan flood in India: 4 dead, ~100 missing",
     "Wall of muddy water tears through a mountain valley; army searches. (AP)"),
    ("HEALTH", "DRC Ebola death toll passes 5,300",
     "Kenya discharges its last Ebola patient as the outbreak toll climbs. (C54)"),
]


def load(path, size):
    return PILFont.truetype(path, size)


def split_lines(draw, text, font, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_header(draw):
    draw.rectangle((0, 0, 1024, 148), fill=DARK)
    draw.rectangle((0, 148, 1024, 152), fill=ACCENT)
    masthead = load(BOLD, 60)
    dateline = load(BOLD, 25)
    draw.text((30, 24), "THE WORLD TODAY", font=masthead, fill=(255, 255, 255))
    draw.text((30, 100), "WORLD NEWS \u2022 TUESDAY 24 NOVEMBER 2026",
              font=dateline, fill=(216, 180, 86))


def paint_row(draw, top, height, index, category, headline, detail):
    if index % 2:
        draw.rectangle((0, top, 1024, top + height), fill=ALT_ROW)
    colour = CATEGORY_COLORS[category]
    draw.rectangle((0, top, 10, top + height), fill=colour)
    tag = load(BOLD, 18)
    head = load(BOLD, 23)
    body = load(PLAIN, 19)
    draw.text((26, top + 14), category, font=tag, fill=colour)
    wrapped = split_lines(draw, headline, head, 840)[:2]
    y = top + 10
    for line in wrapped:
        draw.text((148, y), line, font=head, fill=TEXT)
        y += 27
    draw.text((148, top + 56), detail, font=body, fill=MUTED)


def paint_footer(draw):
    draw.rectangle((0, 982, 1024, 1024), fill=DARK)
    small = load(PLAIN, 17)
    line = "Sources: Kyiv Independent \u2022 NPR \u2022 AP \u2022 FT \u2022 AFP \u2022 EU \u2022 PBS \u2022 C54"
    width = draw.textlength(line, font=small)
    draw.text(((1024 - width) / 2, 998), line, font=small, fill=(255, 255, 255))


def build():
    canvas = PILImage.new("RGB", SIZE, PAPER)
    draw = PILDraw.Draw(canvas)
    paint_header(draw)
    row_height = 83
    for i, (category, headline, detail) in enumerate(NEWS):
        top = 152 + i * row_height
        paint_row(draw, top, row_height, i, category, headline, detail)
        if i < len(NEWS) - 1:
            draw.line((0, top + row_height, 1024, top + row_height), fill=RULE)
    paint_footer(draw)
    canvas.save("news.png")
    print(f"saved news.png {canvas.size[0]}x{canvas.size[1]}")


if __name__ == "__main__":
    build()
