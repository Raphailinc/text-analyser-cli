from __future__ import annotations

from pathlib import Path

from text_analyser import ocr


def test_generate_and_enhance(tmp_path: Path):
    img_path = tmp_path / "sample.png"
    ocr.generate_sample("Hello OCR", img_path)
    assert img_path.exists()

    result = ocr.extract_text(
        img_path,
        runner=lambda image, **_: "stub",
        save_enhanced=tmp_path / "enhanced.png",
    )
    assert result.text == "stub"
    assert result.enhanced_path and result.enhanced_path.exists()


def test_iter_lines():
    lines = list(ocr.iter_lines("a\n\nb  \n c"))
    assert lines == ["a", "b", "c"]
