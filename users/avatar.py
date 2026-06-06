import hashlib
import io
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    AVATAR_TEXT_Y_OFFSET,
)

PRESET_AVATAR_DIR = Path(__file__).resolve().parent.parent / "static" / "images" / "avatars"
PRESET_AVATAR_NAMES = ("Maria", "Alex", "Nikita")

DEMO_AVATAR_FILES = {
    "anna@example.com": "Alex.png",
    "boris@example.com": "Nikita.png",
    "maria@example.com": "Maria.png",
}

def color_for_name(name: str) -> tuple[int, int, int]:
    key = (name or "?").strip().lower()
    index = sum(ord(char) for char in key) % len(AVATAR_COLORS)
    return AVATAR_COLORS[index]


def preset_filename_for_name(name: str) -> str:
    index = sum(ord(char) for char in (name or "?").lower()) % len(PRESET_AVATAR_NAMES)
    return f"{PRESET_AVATAR_NAMES[index]}.png"


def load_preset_avatar_file(filename: str) -> ContentFile:
    path = PRESET_AVATAR_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Preset avatar not found: {path}")
    return ContentFile(path.read_bytes(), name=filename)


def generate_avatar_file(name: str) -> ContentFile:
    letter = (name or "?")[0].upper()
    color = color_for_name(name)
    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color=color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default(size=AVATAR_FONT_SIZE)

    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = (
        (AVATAR_SIZE - text_width) / 2,
        (AVATAR_SIZE - text_height) / 2 - AVATAR_TEXT_Y_OFFSET
    )

    draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    suffix = hashlib.md5(name.encode("utf-8")).hexdigest()[:10]
    return ContentFile(buffer.read(), name=f"avatar_{suffix}.png")
