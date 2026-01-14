from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

try:
    import pytesseract

    _HAS_TESSERACT = True
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None  # type: ignore
    _HAS_TESSERACT = False


@dataclass(slots=True)
class OcrResult:
    text: str
    image_path: Path
    enhanced_path: Path | None = None


def generate_sample(text: str, destination: Path, *, width: int = 1200, height: int = 360) -> Path:
    """Create a high-contrast synthetic image for testing OCR."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((80, height // 3), text, fill="black", font=font)
    image.save(destination)
    return destination


def to_grayscale(image: Image.Image) -> Image.Image:
    return ImageOps.grayscale(image)


def binarize(image: Image.Image, *, threshold: int = 180) -> Image.Image:
    """Simple binarization to improve OCR accuracy."""
    if image.mode != "L":
        image = to_grayscale(image)
    return image.point(lambda p: 255 if p > threshold else 0, mode="1")


def enhance(image: Image.Image, *, invert: bool = False, threshold: int = 180) -> Image.Image:
    img = binarize(image, threshold=threshold)
    if invert:
        img = ImageOps.invert(img.convert("L"))
    return img


def _default_runner(img: Image.Image, *, lang: str, psm: int, oem: int, tesseract_cmd: str | None) -> str:
    if not _HAS_TESSERACT:
        raise ImportError("pytesseract is not installed; install it or provide a custom runner.")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    return pytesseract.image_to_string(img, lang=lang, config=f"--psm {psm} --oem {oem}")


def extract_text(
    image_path: Path,
    *,
    lang: str = "eng",
    psm: int = 6,
    oem: int = 3,
    invert: bool = False,
    threshold: int = 180,
    tesseract_cmd: str | None = None,
    runner: Callable[..., str] = _default_runner,
    save_enhanced: Path | None = None,
) -> OcrResult:
    """Load an image, enhance it for OCR, and extract text."""

    if not image_path.exists():
        raise FileNotFoundError(image_path)

    image = Image.open(image_path)
    enhanced = enhance(image, invert=invert, threshold=threshold)

    if save_enhanced:
        save_enhanced.parent.mkdir(parents=True, exist_ok=True)
        enhanced.save(save_enhanced)

    text = runner(enhanced, lang=lang, psm=psm, oem=oem, tesseract_cmd=tesseract_cmd)
    return OcrResult(text=text, image_path=image_path, enhanced_path=save_enhanced)


def iter_lines(text: str) -> Iterable[str]:
    return (line.strip() for line in text.splitlines() if line.strip())
