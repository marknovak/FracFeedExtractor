import pytest
import json
import joblib
from pathlib import Path
from src.model.train_model import load_labeled_data, train_pdf_classifier


@pytest.fixture
def sample_data(tmp_path):
    data_dir = tmp_path / "data" / "processed-text"
    data_dir.mkdir(parents=True)
    labels_file = tmp_path / "data" / "labels.json"

    (data_dir / "useful1.txt").write_text("predator diet stomach contents", encoding="utf-8")
    (data_dir / "useful2.txt").write_text("prey composition and feeding habits", encoding="utf-8")
    (data_dir / "useful3.txt").write_text("feeding behavior and prey analysis", encoding="utf-8")
    (data_dir / "notuseful1.txt").write_text("study of unrelated mineral content", encoding="utf-8")
    (data_dir / "notuseful2.txt").write_text("random geological paper unrelated", encoding="utf-8")
    (data_dir / "notuseful3.txt").write_text("chemical structure of basalt samples", encoding="utf-8")

    labels = {"useful1.txt": "useful", "useful2.txt": "useful", "useful3.txt": "useful", "notuseful1.txt": "not useful", "notuseful2.txt": "not useful", "notuseful3.txt": "not useful"}
    with open(labels_file, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=4)

    return data_dir, labels_file


def test_load_labeled_data_reads_all(sample_data):
    data_dir, labels_file = sample_data
    texts, labels, filenames = load_labeled_data(data_dir, labels_file)

    assert len(texts) == 6
    assert len(labels) == 6
    assert set(labels) == {"useful", "not useful"}
    assert all(name.endswith(".txt") for name in filenames)


def test_load_labeled_data_warns_for_missing_label(tmp_path, capsys):
    data_dir = tmp_path / "data" / "processed-text"
    data_dir.mkdir(parents=True)
    (data_dir / "extra.txt").write_text("content", encoding="utf-8")

    labels_file = tmp_path / "data" / "labels.json"
    with open(labels_file, "w", encoding="utf-8") as f:
        json.dump({}, f)

    load_labeled_data(data_dir, labels_file)
    captured = capsys.readouterr()
    assert "[WARN]" in captured.out


def test_train_pdf_classifier_creates_model_and_vectorizer(sample_data, tmp_path):
    data_dir, labels_file = sample_data
    texts, labels, _ = load_labeled_data(data_dir, labels_file)

    output_dir = tmp_path / "models"
    result = train_pdf_classifier(texts, labels, output_dir)

    assert result is not None, "Training should return a result dictionary"
    assert "accuracy" in result
    assert (output_dir / "pdf_classifier_model.pkl").exists()
    assert (output_dir / "tfidf_vectorizer.pkl").exists()

    # Confirm model and vectorizer load successfully
    model = joblib.load(output_dir / "pdf_classifier_model.pkl")
    vectorizer = joblib.load(output_dir / "tfidf_vectorizer.pkl")
    assert model is not None
    assert vectorizer is not None


def test_train_pdf_classifier_handles_empty_data(capsys):
    result = train_pdf_classifier([], [])
    captured = capsys.readouterr()
    assert result is None
    assert "[ERROR]" in captured.out


def test_train_pdf_classifier_one_class(capsys):
    texts = ["predator stomach analysis", "diet prey composition"]
    labels = ["useful", "useful"]

    result = train_pdf_classifier(texts, labels)
    captured = capsys.readouterr()
    assert result is None
    assert "Need at least 2 classes" in captured.out


def test_train_pdf_classifier_too_few_per_class(capsys):
    texts = ["useful text", "not useful text"]
    labels = ["useful", "not useful"]

    result = train_pdf_classifier(texts, labels)
    captured = capsys.readouterr()
    assert result is None
    assert "Each class needs at least 2 samples" in captured.out


def test_train_pdf_classifier_output_accuracy_range(sample_data, tmp_path):
    data_dir, labels_file = sample_data
    texts, labels, _ = load_labeled_data(data_dir, labels_file)

    output_dir = tmp_path / "models"
    result = train_pdf_classifier(texts, labels, output_dir)

    assert result is not None, "train_pdf_classifier should return a result"
    assert isinstance(result["accuracy"], float)
    assert 0.0 <= result["accuracy"] <= 1.0
