# Text Analyser CLI

[![CI](https://github.com/Raphailinc/text-analyser-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/text-analyser-cli/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

A command-line OCR experiment with image preprocessing and a reusable Python module.

## What it does

- Run Tesseract on an input image with configurable language and engine options.
- Adjust contrast, inversion and thresholding before recognition.
- Generate a synthetic text image for a local demonstration.
- Test application behavior with an OCR stub.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m text_analyser.cli sample "Demo text" tmp/sample.png
python -m text_analyser.cli ocr tmp/sample.png --lang eng --json
```

## Checks

```bash
python -m pytest
```

## Scope and implementation notes

Real OCR requires the Tesseract executable and requested language packs. Unit tests use a stub and do not measure recognition accuracy.
