import pytest
import joblib
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.model.pdf_classifier import classify_pdf


@pytest.fixture
def model_dir_with_mock_model(tmp_path):
    model_dir = tmp_path / "models"
    model_dir.mkdir(parents=True)

    # Create a mock model and vectorizer
    mock_model = MagicMock()
    mock_model.predict.return_value = ["useful"]
    mock_model.predict_proba.return_value = [[0.2, 0.8]]

    mock_vectorizer = MagicMock()
    mock_vectorizer.transform.return_value = "fake_transformed_data"

    # Save mock objects
    joblib.dump(mock_model, model_dir / "pdf_classifier_model.pkl")
    joblib.dump(mock_vectorizer, model_dir / "tfidf_vectorizer.pkl")

    return model_dir


@patch("src.model.pdf_classifier.extract_text_from_pdf", return_value="predator stomach content analysis")
def test_classify_pdf_valid_case(mock_extract, model_dir_with_mock_model, capsys):
    test_pdf = Path("tests/test.pdf")
    classify_pdf(test_pdf, model_dir_with_mock_model)

    output = capsys.readouterr().out
    assert "PDF Classification Result" in output
    assert "useful" in output.lower()
    assert "%" in output


def test_classify_pdf_missing_model(capsys, tmp_path):
    model_dir = tmp_path / "empty_models"
    model_dir.mkdir()

    test_pdf = Path("tests/test.pdf")
    classify_pdf(test_pdf, model_dir)

    output = capsys.readouterr().out
    assert "[ERROR]" in output
    assert "Missing model" in output


@patch("src.model.pdf_classifier.extract_text_from_pdf", return_value="")
def test_classify_pdf_no_text(mock_extract, model_dir_with_mock_model, capsys):
    test_pdf = Path("tests/empty.pdf")
    classify_pdf(test_pdf, model_dir_with_mock_model)

    output = capsys.readouterr().out
    assert "[ERROR]" in output
    assert "No text extracted" in output


@patch("src.model.pdf_classifier.extract_text_from_pdf", return_value="diet prey stomach analysis")
def test_classify_pdf_confidence_and_prediction(mock_extract, model_dir_with_mock_model, capsys):
    test_pdf = Path("tests/valid.pdf")
    classify_pdf(test_pdf, model_dir_with_mock_model)

    output = capsys.readouterr().out
    assert "Prediction:" in output
    assert "Confidence" not in output
    assert "useful" in output.lower()


def test_classify_pdf_handles_nonexistent_model_dir(tmp_path, capsys):
    model_dir = tmp_path / "nonexistent_dir"
    test_pdf = Path("tests/missing_model.pdf")

    classify_pdf(test_pdf, model_dir)

    output = capsys.readouterr().out
    assert "[ERROR]" in output
    assert "Missing model" in output
