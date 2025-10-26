from src.preprocessing.pdf_text_extraction import extract_text_from_pdf
from pathlib import Path

def test_extract_text_exists():
    pdf_path = Path("tests/test.pdf")
    text = extract_text_from_pdf(str(pdf_path))
    assert text is not None
    assert len(text) > 0