from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .ocr import OcrResult, extract_text, generate_sample


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Lightweight OCR CLI")
    parser.add_argument("--version", action="version", version=f"text-analyser {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    ocr = subparsers.add_parser("ocr", help="Run OCR on an image")
    ocr.add_argument("image", type=Path, help="Path to image file")
    ocr.add_argument("--lang", default="eng", help="Tesseract language(s), e.g. 'eng+rus'")
    ocr.add_argument("--psm", type=int, default=6, help="Page segmentation mode (psm)")
    ocr.add_argument("--oem", type=int, default=3, help="OCR Engine Mode (oem)")
    ocr.add_argument("--invert", action="store_true", help="Invert colors before OCR")
    ocr.add_argument("--threshold", type=int, default=180, help="Binarization threshold 0-255")
    ocr.add_argument("--save-enhanced", type=Path, help="Save enhanced image to this path")
    ocr.add_argument("--tesseract-cmd", type=str, help="Path to tesseract binary")
    ocr.add_argument("--json", action="store_true", help="Output JSON instead of plain text")
    ocr.set_defaults(handler=handle_ocr)

    sample = subparsers.add_parser("sample", help="Generate synthetic sample image")
    sample.add_argument("text", help="Text to render")
    sample.add_argument("destination", type=Path, help="Where to save the image")
    sample.add_argument("--width", type=int, default=1200)
    sample.add_argument("--height", type=int, default=360)
    sample.set_defaults(handler=handle_sample)

    return parser


def handle_ocr(args: argparse.Namespace) -> None:
    result = extract_text(
        args.image,
        lang=args.lang,
        psm=args.psm,
        oem=args.oem,
        invert=args.invert,
        threshold=args.threshold,
        tesseract_cmd=args.tesseract_cmd,
        save_enhanced=args.save_enhanced,
    )
    emit_result(result, as_json=args.json)


def handle_sample(args: argparse.Namespace) -> None:
    path = generate_sample(args.text, args.destination, width=args.width, height=args.height)
    print(f"Sample saved to {path}")


def emit_result(result: OcrResult, *, as_json: bool) -> None:
    if as_json:
        payload: dict[str, Any] = {
            "text": result.text,
            "image_path": str(result.image_path),
        }
        if result.enhanced_path:
            payload["enhanced_path"] = str(result.enhanced_path)
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(result.text.strip())


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.handler(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
