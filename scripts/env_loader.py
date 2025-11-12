"""Load environment variables from .env file for local development."""

from pathlib import Path


def load_env():
    """Load .env file from repo root if it exists."""
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.exists():
        return  # No .env file, assume env vars set manually or in CI

    import os

    with env_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
