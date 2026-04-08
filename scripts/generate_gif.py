#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import os
import sys
import json
import re
import urllib.request


def get_murder_count() -> int:
    try:
        req = urllib.request.Request(
            "https://transmurdermonitoring.tgeu.org/library/"
            "?q=(allAggregations:!t,from:0,includeUnpublished:!t,"
            "limit:30,order:asc,sort:metadata.tdor_period__oct_sept_,"
            "treatAs:number,unpublished:!f)",
            headers={"User-Agent": "readme-bot"},
        )
        html = urllib.request.urlopen(req, timeout=15).read().decode()
        m = re.search(r"of\s+\*?\*?(\d[\d,]+)\*?\*?\s+entities", html)
        if m:
            return int(m.group(1).replace(",", ""))
    except Exception:
        pass
    return 5320


COUNT = str(get_murder_count())

WORDS = [
    COUNT,
    "confirmed cases",
    "of trans genocide",
    "support trans rights",
]

WIDTH, HEIGHT = 480, 120
TRANS_COLORS = [(85, 205, 252), (247, 168, 184), (255, 255, 255), (247, 168, 184), (85, 205, 252)]
STRIPE_H = HEIGHT // len(TRANS_COLORS)
OUTPUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gif.gif")


def draw_flag(draw: ImageDraw.ImageDraw) -> None:
    for i, color in enumerate(TRANS_COLORS):
        y0 = i * STRIPE_H
        y1 = y0 + STRIPE_H if i < len(TRANS_COLORS) - 1 else HEIGHT
        draw.rectangle([0, y0, WIDTH, y1], fill=color)


def get_font(size: int) -> ImageFont.FreeTypeFont:
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def build_palette() -> Image.Image:
    ref = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(ref)
    draw_flag(draw)
    font = get_font(28)
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            draw.text((10 + dx, 10 + dy), "palette ref", font=font, fill=(0, 0, 0))
    draw.text((10, 10), "palette ref", font=font, fill=(255, 255, 255))
    return ref.quantize(colors=128)


def make_frame(text: str, palette_img: Image.Image) -> Image.Image:
    frame = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(frame)
    draw_flag(draw)
    font = get_font(28)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (WIDTH - tw) // 2
    y = (HEIGHT - th) // 2
    for dx in (-2, -1, 0, 1, 2):
        for dy in (-2, -1, 0, 1, 2):
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    return frame.quantize(palette=palette_img, dither=0)


def main() -> None:
    palette_img = build_palette()
    frames = [make_frame(w, palette_img) for w in WORDS]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=1200,
        loop=0,
    )
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
