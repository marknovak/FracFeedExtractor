"""Google Drive I/O utilities using a Service Account.

Environment variables required:
 - GOOGLE_SERVICE_ACCOUNT_JSON: JSON string of the service account credentials
 - GOOGLE_DRIVE_ROOT_FOLDER_ID: ID of the root folder containing 'useful' and 'not-useful'

Optional:
 - GOOGLE_DRIVE_USE_SHARED_DRIVE=true (enables includeItemsFromAllDrives/supportsAllDrives)

This module streams PDF bytes without saving the PDF to disk.
"""

from __future__ import annotations

import os
import io
import re
from typing import List, Dict, Optional, Tuple

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from scripts.env_loader import load_env

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _use_all_drives() -> bool:
    return os.environ.get("GOOGLE_DRIVE_USE_SHARED_DRIVE", "false").lower() in {"1", "true", "yes"}


def get_drive_service():
    load_env()  # Load .env file if present
    creds_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_info:
        raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON environment variable")

    import json

    creds = service_account.Credentials.from_service_account_info(json.loads(creds_info), scopes=SCOPES)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def find_child_folder_id(service, parent_id: str, name: str) -> Optional[str]:
    q = f"mimeType = 'application/vnd.google-apps.folder' and name = '{name}' and '{parent_id}' in parents and trashed = false"
    params = {
        "q": q,
        "fields": "files(id, name)",
        "pageSize": 10,
    }
    if _use_all_drives():
        params.update({
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True,
        })
    resp = service.files().list(**params).execute()
    files = resp.get("files", [])
    return files[0]["id"] if files else None


def list_pdfs_in_folder(service, folder_id: str, max_files: Optional[int] = None, order_desc: bool = True) -> List[Dict]:
    q = f"'{folder_id}' in parents and mimeType = 'application/pdf' and trashed = false"
    params = {
        "q": q,
        "fields": "nextPageToken, files(id, name, mimeType, modifiedTime)",
        "pageSize": 100,
        "orderBy": "modifiedTime desc" if order_desc else "modifiedTime",
    }
    if _use_all_drives():
        params.update({
            "supportsAllDrives": True,
            "includeItemsFromAllDrives": True,
        })

    results: List[Dict] = []
    while True:
        resp = service.files().list(**params).execute()
        results.extend(resp.get("files", []))
        if max_files and len(results) >= max_files:
            return results[:max_files]
        token = resp.get("nextPageToken")
        if not token:
            break
        params["pageToken"] = token
    return results


def download_file_bytes(service, file_id: str) -> bytes:
    request = service.files().get_media(fileId=file_id, supportsAllDrives=_use_all_drives())
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request, chunksize=1024 * 1024)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        # Optionally, could print progress: status.progress()
    return buf.getvalue()


def sanitize_filename(name: str) -> str:
    # Remove extension for stem-like behavior
    name = re.sub(r"\.[Pp][Dd][Ff]$", "", name)
    # Replace unsafe chars with underscore
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
    if not name:
        name = "file"
    return name
