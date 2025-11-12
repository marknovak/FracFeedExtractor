"""CI pipeline: stream a small, fixed sample from Google Drive and run extraction.

Requirements:
 - Env GOOGLE_SERVICE_ACCOUNT_JSON set to Service Account JSON string.
 - Env GOOGLE_DRIVE_ROOT_FOLDER_ID set to the Drive folder containing 'useful' and 'not-useful'.
 - Optional env CI_FILES_PER_CLASS (default 1).

This script DOES NOT save PDFs locally. It streams bytes and writes extracted text
into data/processed-text/*.txt, and writes data/labels.json. No training.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict, List
import subprocess

import sys
from pathlib import Path as _Path
sys.path.append(str(_Path(__file__).resolve().parents[1]))  # add repo root to sys.path

from scripts.env_loader import load_env
load_env()  # Load .env file if present (for local dev)

from scripts.drive_io import (
    get_drive_service,
    find_child_folder_id,
    list_pdfs_in_folder,
    download_file_bytes,
    sanitize_filename,
)
from src.preprocessing.pdf_text_extraction import extract_text_from_pdf_bytes


def write_labels(labels: Dict[str, str], output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2)


def main():
    root_id = os.environ.get("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    if not root_id:
        raise RuntimeError("Missing GOOGLE_DRIVE_ROOT_FOLDER_ID environment variable")

    per_class = 20  # Fixed set size for CI

    service = get_drive_service()
    useful_id = find_child_folder_id(service, root_id, "useful")
    not_useful_id = find_child_folder_id(service, root_id, "not-useful")
    if not useful_id:
        raise RuntimeError(f"Could not find 'useful' subfolder under root folder {root_id}")
    if not not_useful_id:
        raise RuntimeError(f"Could not find 'not-useful' subfolder under root folder {root_id}")

    # Prepare output directory
    out_dir = Path("data/processed-text")
    out_dir.mkdir(parents=True, exist_ok=True)

    labels: Dict[str, str] = {}

    for folder_id, label in [(useful_id, "useful"), (not_useful_id, "not useful")]:
        files = list_pdfs_in_folder(service, folder_id, max_files=per_class)
        for f in files:
            pdf_name = f.get("name", f.get("id", "file"))
            print(f"[CI] Processing: {pdf_name} ({label})")
            pdf_bytes = download_file_bytes(service, f["id"])
            text = extract_text_from_pdf_bytes(pdf_bytes)
            stem = sanitize_filename(pdf_name)
            txt_name = f"{stem}.txt"
            (out_dir / txt_name).write_text(text, encoding="utf-8")
            labels[txt_name] = label
            print(f"[CI]   ✓ Extracted to {txt_name}")

    write_labels(labels, Path("data/labels.json"))
    print(f"[CI] Wrote {len(labels)} labels and extracted text files to {out_dir}")

    # Train model on the CI sample
    print("[CI] Training model on CI sample...")
    r = subprocess.run([sys.executable, "src/model/train_model.py"], env={**os.environ, "CI_TRAIN": "1"})
    if r.returncode != 0:
        raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
