"""
Constants utilized throughout the project
"""

from pathlib import Path

BASE_URL = "https://api.spotify.com/v1/"

REDIRECT_URL = "http://localhost:8888/callback"

AUTH_URL = "https://accounts.spotify.com/api/token"

BASE_PATH = Path(__file__).resolve()

REPO_ROOT = BASE_PATH.parent.parent

DATA_DIRECTORY = REPO_ROOT / "data" / "raw"

PROCESSED_DIRECTORY = REPO_ROOT / "data" / "processed"
