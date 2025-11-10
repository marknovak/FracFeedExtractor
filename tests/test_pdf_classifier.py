import pytest
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from unittest.mock import patch, MagicMock
from src.model.pdf_classifier import classify_pdf


@pytest.fixture
def model_dir_with_mock_model(tmp_path):
    model_dir = tmp_path / "models"
    model_dir.mkdir(parents=True)

    texts = ["predator stomach content", "fish prey analysis", "rock study geology", "mineral content paper"]
    labels = ["useful", "useful", "not useful", "not useful"]

    vectorizer = TfidfVectorizer(max_features=4)
    X = vectorizer.fit_transform(texts)
    model = LogisticRegression().fit(X, labels)

    joblib.dump(model, model_dir / "pdf_classifier_model.pkl")
    joblib.dump(vectorizer, model_dir / "tfidf_vectorizer.pkl")

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
