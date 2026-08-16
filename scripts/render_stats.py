from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": (10, 10, 10),
        "accent": (125, 211, 252),
        "title": (245, 245, 245),
        "label": (163, 163, 163),
        "value": (245, 245, 245),
        "track": (38, 38, 38),
        "rule": (38, 38, 38),
    },
    "light": {
        "bg": (246, 246, 244),
        "accent": (2, 132, 199),
        "title": (17, 17, 17),
        "label": (82, 82, 82),
        "value": (17, 17, 17),
        "track": (229, 229, 226),
        "rule": (229, 229, 226),
    },
}

STATS = [
    ("Contributions this year", "296"),
    ("Repositories", "15"),
    ("Pull requests", "67"),
    ("Issues opened", "92"),
]

LANGUAGES = [
    ("Python", 0.61, (53, 114, 165)),
    ("C++", 0.29, (243, 75, 125)),
    ("TypeScript", 0.10, (49, 120, 198)),
]


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fonts() -> tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
    title = load_font(
        [r"C:\Windows\Fonts\segoeuisemibold.ttf", r"C:\Windows\Fonts\segoeuib.ttf"],
        22,
    )
    body = load_font([r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"], 18)
    mono = load_font([r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"], 16)
    return title, body, mono


def rounded_card(size: tuple[int, int], theme: dict) -> Image.Image:
    image = Image.new("RGB", size, theme["bg"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, size[0], 3), fill=theme["accent"])
    return image


def render_stats(theme_name: str) -> None:
    theme = THEMES[theme_name]
    title_font, body, mono = fonts()
    image = rounded_card((520, 236), theme)
    draw = ImageDraw.Draw(image)
    draw.text((28, 22), "GitHub activity", fill=theme["title"], font=title_font)
    draw.text((28, 50), "Includes private repositories", fill=theme["label"], font=mono)

    for index, (label, value) in enumerate(STATS):
        row = 88 + index * 34
        draw.text((28, row), label, fill=theme["label"], font=body)
        draw.text((360, row), value, fill=theme["value"], font=title_font)

    image.save(ASSETS / f"stats-{theme_name}.png", optimize=True)


def render_languages(theme_name: str) -> None:
    theme = THEMES[theme_name]
    title_font, body, mono = fonts()
    image = rounded_card((400, 236), theme)
    draw = ImageDraw.Draw(image)
    draw.text((28, 22), "Languages", fill=theme["title"], font=title_font)
    draw.text((28, 50), "Weighted by source size", fill=theme["label"], font=mono)

    bar_left, bar_right = 28, 372
    for index, (name, share, color) in enumerate(LANGUAGES):
        row = 96 + index * 42
        draw.text((bar_left, row), name, fill=theme["label"], font=body)
        draw.text((bar_right - 56, row), f"{int(share * 100)}%", fill=theme["value"], font=mono)
        track_top = row + 24
        draw.rectangle((bar_left, track_top, bar_right, track_top + 6), fill=theme["track"])
        draw.rectangle(
            (bar_left, track_top, bar_left + int((bar_right - bar_left) * share), track_top + 6),
            fill=color,
        )

    image.save(ASSETS / f"langs-{theme_name}.png", optimize=True)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for theme_name in THEMES:
        render_stats(theme_name)
        render_languages(theme_name)
