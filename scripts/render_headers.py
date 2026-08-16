from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": (10, 10, 10),
        "accent": (125, 211, 252),
        "name": (245, 245, 245),
        "role": (196, 196, 196),
        "meta": (115, 115, 115),
    },
    "light": {
        "bg": (246, 246, 244),
        "accent": (2, 132, 199),
        "name": (17, 17, 17),
        "role": (64, 64, 64),
        "meta": (115, 115, 115),
    },
}


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render(theme_name: str) -> None:
    theme = THEMES[theme_name]
    image = Image.new("RGB", (1200, 268), theme["bg"])
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 3), fill=theme["accent"])

    mono = load_font(
        [
            r"C:\Windows\Fonts\consola.ttf",
            r"C:\Windows\Fonts\cour.ttf",
        ],
        18,
    )
    title = load_font(
        [
            r"C:\Windows\Fonts\segoeuisemibold.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ],
        58,
    )
    body = load_font(
        [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ],
        24,
    )
    chinese = load_font(
        [
            r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\simhei.ttf",
        ],
        18,
    )

    draw.text((64, 52), "LONDON / UK", fill=theme["meta"], font=mono)
    draw.text((248, 50), "·  李智峰", fill=theme["meta"], font=chinese)
    draw.text((64, 104), "Zhifeng Li", fill=theme["name"], font=title)
    draw.text(
        (64, 178),
        "AI/ML Engineer & Computational Scientist",
        fill=theme["role"],
        font=body,
    )
    draw.text(
        (64, 220),
        "Imperial College London  ·  Microsoft Core AI  ·  MSc ACSE",
        fill=theme["meta"],
        font=mono,
    )
    image.save(ASSETS / f"header-{theme_name}.png", optimize=True)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    render("dark")
    render("light")
