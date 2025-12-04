from __future__ import annotations

from pathlib import Path

from src.core.models import RawContent


def load_content(path: str) -> RawContent:
    """Load raw text content from a Markdown or plain-text file."""

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Content file not found: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    return RawContent(path=str(file_path), text=text)
