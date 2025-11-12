"""Full training pipeline: stream ALL PDFs from Drive, extract text, label, train model.

Environment variables:
 - GOOGLE_SERVICE_ACCOUNT_JSON (service account JSON string)
 - GOOGLE_DRIVE_ROOT_FOLDER_ID (root folder containing 'useful' and 'not-useful')
 - GOOGLE_DRIVE_USE_SHARED_DRIVE=true (if using shared drives / shared folders)

Behavior:
 - Streams every PDF (no local PDF persistence) and writes extracted text to data/processed-text.
 - Generates labels.json based on folder origin.
 - Trains model with src/model/train_model.py.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Dict
import subprocess
import sys

import sys
from pathlib import Path as _Path2
sys.path.append(str(_Path2(__file__).resolve().parents[1]))  # add repo root to sys.path

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


def run(cmd):
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(r.returncode)


def write_labels(labels: Dict[str, str], output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2)


def main():
    root_id = os.environ.get("GOOGLE_DRIVE_ROOT_FOLDER_ID")
    if not root_id:
        raise RuntimeError("Missing GOOGLE_DRIVE_ROOT_FOLDER_ID environment variable")

    service = get_drive_service()
    useful_id = find_child_folder_id(service, root_id, "useful")
    not_useful_id = find_child_folder_id(service, root_id, "not-useful")
    if not useful_id:
        raise RuntimeError(f"Could not find 'useful' subfolder under root folder {root_id}")
    if not not_useful_id:
        raise RuntimeError(f"Could not find 'not-useful' subfolder under root folder {root_id}")

    out_dir = Path("data/processed-text")
    out_dir.mkdir(parents=True, exist_ok=True)
    labels: Dict[str, str] = {}

    for folder_id, label in [(useful_id, "useful"), (not_useful_id, "not-useful")]:
        files = list_pdfs_in_folder(service, folder_id, max_files=None)
        print(f"[FULL] Found {len(files)} PDFs in folder label '{label}'")
        for f in files:
            pdf_bytes = download_file_bytes(service, f["id"])
            text = extract_text_from_pdf_bytes(pdf_bytes)
            stem = sanitize_filename(f.get("name", f.get("id", "file")))
            txt_name = f"{stem}.txt"
            (out_dir / txt_name).write_text(text, encoding="utf-8")
            labels[txt_name] = label

    write_labels(labels, Path("data/labels.json"))
    print(f"[FULL] Wrote {len(labels)} labeled text files. Beginning model training...")

    # Train model
    run([sys.executable, "src/model/train_model.py"])
    print("[FULL] Training complete.")


if __name__ == "__main__":
    main()
