# text-analyser-cli

Упрощённый CLI для OCR на базе Pillow + Tesseract. Без Django/GUI — только удобные команды, синтетические примеры и базовые автотесты.

## Установка
```bash
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Убедитесь, что `tesseract` установлен и доступен в PATH (или передайте `--tesseract-cmd`).

## Использование
```bash
# OCR
python -m text_analyser.cli ocr path/to/image.png --lang eng+rus --save-enhanced out/enhanced.png --json

# Генерация синтетического образца
python -m text_analyser.cli sample "Demo text" tmp/sample.png

# Коротко
python -m text_analyser.cli --help
```

Опции OCR:
- `--lang` — языки Tesseract (`eng`, `rus+eng`, ...).
- `--psm`/`--oem` — режимы Tesseract.
- `--invert`/`--threshold` — простая обработка для повышения контраста.
- `--save-enhanced` — сохранить улучшенное изображение перед OCR.
- `--tesseract-cmd` — путь к исполняемому файлу Tesseract, если не в PATH.
- `--json` — вернуть JSON с путём к файлам.

## Тесты
```bash
pytest
```
(использует заглушку OCR, поэтому Tesseract не требуется для тестов.)

## Структура
- `text_analyser/ocr.py` — генерация образца, улучшение изображения, вызов OCR.
- `text_analyser/cli.py` — argparse CLI.
- `tests/` — автотесты (pytest).
- `requirements.txt` — зависимости.
