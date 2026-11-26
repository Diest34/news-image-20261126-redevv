#!/usr/bin/env python3
"""Compose the entry image for 26 November 2026 world news.

Builds a 1024x1024 newspaper front page from three photo panels made
for this entry (assets/panel-*.jpg) plus the day's headlines, drawn with
Pillow. Run from this directory:

    python3 build_image.py

Writes entry.png next to this script. Deterministic: same inputs give
the same bytes (Pillow writes no timestamps into PNGs).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
WIDTH = 1024
HEIGHT = 1024

NAVY = (15, 41, 74)
GOLD = (217, 164, 65)
PAPER = (255, 255, 255)
INK = (18, 18, 18)
GREY = (88, 94, 102)
LIGHT_GREY = (200, 205, 212)
MASTHEAD_SUB = (185, 199, 216)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

# (tag text, tag colour, headline, deck)
STORIES = [
    (
        "OIL",
        (178, 34, 34),
        "Houthis claim strike on Saudi's biggest refinery",
        "Brent crude tops $94 as Yemen's rebels say they hit Ras Tanura and Riyadh.",
    ),
    (
        "TARIFFS",
        (31, 58, 95),
        "Trump proposes new tariffs on 14 trading partners",
        "China faces the highest rates in a drive against factory overcapacity.",
    ),
    (
        "NUCLEAR",
        (96, 44, 130),
        "Kim orders tactical nuclear weapons spread wider",
        "North Korea says it will deploy the weapons across more domains.",
    ),
    (
        "UKRAINE",
        (24, 110, 62),
        "Kyiv says it struck a major Russian air base",
        "Ukraine reports five planes damaged in a strike deep inside Russia.",
    ),
    (
        "CAIRO",
        (176, 92, 8),
        "Fuel tanker crash fire kills at least 30 in Cairo",
        "A collision on a highway ringing the Egyptian capital ignites a blaze.",
    ),
]

ALSO = (
    "Also: Norway's top court voids disputed oil licences \u00b7 "
    "BepiColombo reaches Mercury orbit \u00b7 Nvidia put on downgrade watch \u00b7 "
    "Duran Duran's Andy Taylor dies at 65"
)

FOOTER = "One day, five stories: fire, tariffs, nukes, a strike, a blaze."
BOTTOM = (
    "World news of Thursday, 26 November 2026 \u00b7 "
    "One image, five stories, one day."
)


def fit_font(draw: ImageDraw.ImageDraw, text: str, name: str,
             start: int, limit: int, minimum: int = 20) -> ImageFont.FreeTypeFont:
    """Largest font size at which *text* fits within *limit* pixels."""
    size = start
    while size > minimum:
        f = font(name, size)
        if draw.textlength(text, font=f) <= limit:
            return f
        size -= 1
    return font(name, minimum)


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont,
         limit: int) -> list[str]:
    """Greedy word wrap of *text* to lines no wider than *limit*."""
    lines: list[str] = []
    current = ""
    for word in text.split(" "):
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=f) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(canvas: Image.Image, path: Path, x: int, y: int,
               w: int, h: int, centering: tuple[float, float] = (0.5, 0.5)) -> None:
    photo = Image.open(path).convert("RGB")
    photo = ImageOps.fit(photo, (w, h), Image.LANCZOS, centering=centering)
    canvas.paste(photo, (x, y))


def build() -> Image.Image:
    canvas = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(canvas)

    # --- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, WIDTH, 148], fill=NAVY)
    f_kicker = font(SANS_BOLD, 29)
    draw.text((32, 18), "THE WORLD IN ONE IMAGE", font=f_kicker, fill=GOLD)
    f_date = fit_font(draw, "Thursday, 26 November 2026", SERIF_BOLD, 62, 960)
    draw.text((30, 50), "Thursday, 26 November 2026", font=f_date, fill=PAPER)
    f_sub = font(SANS, 24)
    draw.text(
        (32, 116),
        "The day's world news, summed up in a single picture",
        font=f_sub, fill=MASTHEAD_SUB,
    )
    draw.rectangle([0, 146, WIDTH, 150], fill=GOLD)

    # --- Photo row ------------------------------------------------------
    # Centerings keep each panel's subject in frame: the flames sit
    # left of centre in the refinery shot, the missile right of centre.
    panels = [
        ("panel-oil.jpg", (0.30, 0.50)),
        ("panel-ship.jpg", (0.50, 0.45)),
        ("panel-missile.jpg", (0.58, 0.50)),
    ]
    widths = [341, 342, 341]
    x = 0
    for (name, centre), w in zip(panels, widths):
        draw_panel(canvas, HERE / "assets" / name, x, 150, w, 300, centre)
        x += w

    # --- Photo caption --------------------------------------------------
    f_cap = font(SANS, 20)
    draw.text((32, 456), "RAS TANURA  \u00b7  WORLD TRADE  \u00b7  PYONGYANG",
              font=f_cap, fill=GREY)

    # --- Headline list --------------------------------------------------
    y = 492
    for tag, colour, headline, deck in STORIES:
        f_tag = font(SANS_BOLD, 21)
        tag_w = int(draw.textlength(tag, font=f_tag)) + 20
        draw.rounded_rectangle([32, y, 32 + tag_w, y + 34], radius=4, fill=colour)
        draw.text((32 + 10, y + 4), tag, font=f_tag, fill=PAPER)
        head_x = 32 + tag_w + 14
        f_head = fit_font(draw, headline, SANS_BOLD, 29, WIDTH - 32 - head_x)
        draw.text((head_x, y + 1), headline, font=f_head, fill=INK)
        f_deck = font(SANS, 22)
        draw.text((32, y + 40), deck, font=f_deck, fill=GREY)
        draw.line([32, y + 72, WIDTH - 32, y + 72], fill=LIGHT_GREY, width=1)
        y += 80

    # --- Also line ------------------------------------------------------
    f_also = font(SANS, 21)
    also_lines = wrap(draw, ALSO, f_also, WIDTH - 64)
    ay = y + 2
    for line in also_lines:
        draw.text((32, ay), line, font=f_also, fill=INK)
        ay += 27

    # --- Footer band ----------------------------------------------------
    band_y = HEIGHT - 72
    draw.rectangle([0, band_y, WIDTH, HEIGHT - 26], fill=NAVY)
    f_foot = fit_font(draw, FOOTER, SANS_BOLD, 24, WIDTH - 64)
    foot_w = draw.textlength(FOOTER, font=f_foot)
    draw.text(((WIDTH - foot_w) / 2, band_y + 11), FOOTER, font=f_foot, fill=PAPER)

    # --- Bottom line ----------------------------------------------------
    f_bottom = font(SANS, 19)
    bottom_w = draw.textlength(BOTTOM, font=f_bottom)
    draw.text(((WIDTH - bottom_w) / 2, HEIGHT - 23), BOTTOM,
              font=f_bottom, fill=GREY)

    return canvas


def main() -> None:
    image = build()
    out = HERE / "entry.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {image.size[0]}x{image.size[1]})")


if __name__ == "__main__":
    main()
