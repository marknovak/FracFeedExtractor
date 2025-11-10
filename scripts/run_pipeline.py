"""
Run the end-to-end local pipeline:
 - Extract text from PDFs in data/useful and data/not-useful
 - Generate labels.json
 - Optionally train the model (disabled by default)

Usage (PowerShell):
  python scripts/run_pipeline.py
  python scripts/run_pipeline.py --train
"""

import argparse
import subprocess
from pathlib import Path
import sys


def run(cmd: list[str]):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)}", file=sys.stderr)
        sys.exit(result.returncode)


def extract_folder(pdf_dir: Path):
    if not pdf_dir.exists():
        print(f"[WARN] Missing folder: {pdf_dir}")
        return
    for pdf in pdf_dir.glob("*.pdf"):
        run([sys.executable, "src/preprocessing/pdf_text_extraction.py", str(pdf)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true", help="Also train the model after preprocessing")
    args = parser.parse_args()

    # Ensure directories
    Path("data/processed-text").mkdir(parents=True, exist_ok=True)

    # Extract text from both classes
    extract_folder(Path("data/useful"))
    extract_folder(Path("data/not-useful"))

    # Generate labels
    run([sys.executable, "src/preprocessing/generate_labels.py"]) 

    if args.train:
        run([sys.executable, "src/model/train_model.py"])


if __name__ == "__main__":
    main()
