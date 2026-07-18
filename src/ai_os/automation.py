from __future__ import annotations

import os
import subprocess
from pathlib import Path


class DesktopAutomation:
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()

    def open_file(self, path: str) -> str:
        candidate = (self.root / path).resolve()
        if not candidate.exists():
            return f"File not found: {path}"
        os.startfile(str(candidate)) if hasattr(os, "startfile") else None
        return f"Opened {path}"

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        return " ".join(sentences[:max_sentences])
