import pytest
import json
import subprocess
from pathlib import Path
from src.preprocessing.generate_labels import generate_labels


def test_generate_labels_creates_json(tmp_path):
    useful_dir = tmp_path / "data" / "useful"
    not_useful_dir = tmp_path / "data" / "not-useful"
    output_file = tmp_path / "data" / "labels.json"

    # Create mock PDF files
    useful_dir.mkdir(parents=True)
    not_useful_dir.mkdir(parents=True)
    (useful_dir / "useful.pdf").touch()
    (not_useful_dir / "not-useful.pdf").touch()

    # Run function
    generate_labels(useful_dir, not_useful_dir, output_file)

    # Assertions
    assert output_file.exists(), "labels.json should be created"
    with open(output_file, "r", encoding="utf-8") as f:
        labels = json.load(f)

    assert "useful.txt" in labels
    assert "not-useful.txt" in labels
    assert labels["useful.pdf"] == "useful"
    assert labels["not-useful.txt"] == "not useful"
    assert len(labels) == 2


def test_generate_labels_empty_folders(tmp_path):
    useful_dir = tmp_path / "data" / "useful"
    not_useful_dir = tmp_path / "data" / "not-useful"
    output_file = tmp_path / "data" / "labels.json"

    useful_dir.mkdir(parents=True)
    not_useful_dir.mkdir(parents=True)

    generate_labels(useful_dir, not_useful_dir, output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        labels = json.load(f)

    assert labels == {}, "Empty folders should produce an empty JSON"


def test_generate_labels_overwrites_existing(tmp_path):
    output_file = tmp_path / "data" / "labels.json"
    output_file.parent.mkdir(parents=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"old_file.txt": "useful"}, f)

    useful_dir = tmp_path / "data" / "useful"
    not_useful_dir = tmp_path / "data" / "not-useful"
    useful_dir.mkdir(parents=True)
    not_useful_dir.mkdir(parents=True)
    (useful_dir / "new_file.pdf").touch()

    generate_labels(useful_dir, not_useful_dir, output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        labels = json.load(f)

    assert "old_file.txt" not in labels
    assert "new_file.txt" in labels
    assert labels["new_file.txt"] == "useful"


def test_generate_labels_cli(tmp_path):
    data_dir = tmp_path / "data"
    useful_dir = data_dir / "useful"
    not_useful_dir = data_dir / "not-useful"
    useful_dir.mkdir(parents=True)
    not_useful_dir.mkdir(parents=True)
    (useful_dir / "CLI_Test.pdf").touch()
    (not_useful_dir / "CLI_Not.pdf").touch()

    result = subprocess.run(
        ["python", "src/preprocessing/generate_labels.py"],
        capture_output=True,
        text=True,
        cwd=Path("."),
    )
    assert result.returncode == 0
    assert "labels.json created" in result.stdout

    output_file = Path("data/labels.json")
    assert output_file.exists()
    labels = json.loads(output_file.read_text(encoding="utf-8"))
    assert "CLI_Test.txt" in labels
    assert "CLI_Not.txt" in labels
