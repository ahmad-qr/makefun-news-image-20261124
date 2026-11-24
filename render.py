#!/usr/bin/env python3
"""Render the 24 November 2026 world-news infographic (1024x1024 PNG).

Ten verified stories from Tuesday 24 November 2026, drawn with Pillow.
Sources: Kyiv Independent, NPR, AP, FT, AFP, EU, PBS, C54.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 245, 240)
NAVY = (11, 31, 58)
GOLD = (201, 162, 39)
WHITE = (255, 255, 255)
INK = (18, 24, 33)
GREY = (92, 98, 108)
ROW_ALT = (240, 238, 232)
LINE = (214, 210, 202)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# (tag, tag colour, headline, detail line)
STORIES = [
    ("WAR", (158, 32, 32), "Russian war death toll nears 700,000",
     "Leaked government data analysed by media puts deaths near 700,000. (Kyiv Independent)"),
    ("WAR", (158, 32, 32), "Ukrainian drones 'hit Russian warship' off Libya",
     "Zelenskyy says drones struck the warship at a Libyan naval base. (NPR)"),
    ("WAR", (158, 32, 32), "Poland scrambles jets as drone enters its airspace",
     "Air defences activated near Dorohusk during overnight strikes on Ukraine."),
    ("TECH", (30, 80, 160), "Nvidia board reinstates Jensen Huang as CEO",
     "Board unanimously restores Huang after resignation and espionage probes. (AP)"),
    ("MARKETS", (150, 110, 20), "Trump 'made up to $15m' on Nvidia shares",
     "FT reports Trump's gains after Huang's return to Nvidia. (FT)"),
    ("CLIMATE", (176, 74, 28), "COP31 climate talks break down",
     "Negotiations in Turkiye collapse over fossil-fuel phase-out language. (AFP)"),
    ("POLITICS", (24, 110, 88), "EU unveils 22nd sanctions package on Russia",
     "New measures target Moscow's war economy and sanctions evasion. (EU)"),
    ("US", (30, 80, 160), "ICE arrests at Seattle airport spark outcry",
     "Father and daughter detained en route to a family baptism. (PBS)"),
    ("DISASTER", (120, 72, 160), "Himalayan flood in India: 4 dead, ~100 missing",
     "Wall of muddy water tears through a mountain valley; army searches. (AP)"),
    ("HEALTH", (24, 110, 88), "DRC Ebola death toll passes 5,300",
     "Kenya discharges its last Ebola patient as the outbreak toll climbs. (C54)"),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ---- Header ----
    draw.rectangle([0, 0, W, 150], fill=NAVY)
    draw.rectangle([0, 150, W, 154], fill=GOLD)
    title_font = font(FONT_BOLD, 62)
    date_font = font(FONT_BOLD, 26)
    draw.text((28, 22), "THE WORLD TODAY", font=title_font, fill=WHITE)
    draw.text((28, 104), "WORLD NEWS  •  TUESDAY 24 NOVEMBER 2026",
              font=date_font, fill=(214, 178, 84))

    # ---- Story rows ----
    head_font = font(FONT_BOLD, 23)
    detail_font = font(FONT_REG, 18)
    tag_font = font(FONT_BOLD, 19)
    row_h = 83
    y0 = 154
    for i, (tag, colour, headline, detail) in enumerate(STORIES):
        top = y0 + i * row_h
        if i % 2 == 1:
            draw.rectangle([0, top, W, top + row_h], fill=ROW_ALT)
        draw.rectangle([0, top, 12, top + row_h], fill=colour)
        draw.text((28, top + 12), tag, font=tag_font, fill=colour)
        lines = wrap(draw, headline, head_font, 850)[:2]
        ly = top + 10
        for line in lines:
            draw.text((150, ly), line, font=head_font, fill=INK)
            ly += 27
        draw.text((150, top + 56), detail, font=detail_font, fill=GREY)
        if i < len(STORIES) - 1:
            draw.line([(0, top + row_h), (W, top + row_h)], fill=LINE, width=1)

    # ---- Footer ----
    draw.rectangle([0, 980, W, H], fill=NAVY)
    foot_font = font(FONT_REG, 17)
    foot = "Sources: Kyiv Independent  •  NPR  •  AP  •  FT  •  AFP  •  EU  •  PBS  •  C54"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, 997), foot, font=foot_font, fill=WHITE)

    img.save("news.png", "PNG")
    print("wrote news.png", img.size)


if __name__ == "__main__":
    main()
