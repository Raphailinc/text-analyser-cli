# Text Analyser CLI

[![CI](https://github.com/Raphailinc/text-analyser-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphailinc/text-analyser-cli/actions/workflows/ci.yml)

[English](README.md) · [Русский](README.ru.md)

Консольный OCR-эксперимент с предварительной обработкой изображений и переиспользуемым Python-модулем.

## Возможности

- Запуск Tesseract с настройкой языка и режима распознавания.
- Контраст, инверсия и пороговая обработка изображения.
- Генерация синтетического текста для демонстрации.
- Проверка поведения приложения с подменой OCR-движка.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m text_analyser.cli sample "Demo text" tmp/sample.png
python -m text_analyser.cli ocr tmp/sample.png --lang eng --json
```

## Проверки

```bash
python -m pytest
```

## Условия запуска и границы проекта

Для реального OCR нужен установленный Tesseract и языковые пакеты. Тесты используют подмену движка и не измеряют точность распознавания.
