from __future__ import annotations

import os
from pathlib import Path
from typing import Any


class ReminderManager:
    def __init__(self, storage_path: str | None = None) -> None:
        self.storage_path = Path(storage_path or Path(__file__).resolve().parents[2] / "reminders.json")
        self.reminders: list[dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        try:
            import json
            self.reminders = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            self.reminders = []

    def _save(self) -> None:
        self.storage_path.write_text(__import__("json").dumps(self.reminders, indent=2), encoding="utf-8")

    def add(self, text: str) -> str:
        self.reminders.append({"text": text, "status": "pending"})
        self._save()
        return f"Reminder added: {text}"

    def list(self) -> list[dict[str, str]]:
        return self.reminders


class FileSearchTool:
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()

    def search(self, query: str, max_results: int = 5) -> list[str]:
        matches: list[str] = []
        if not self.root.exists():
            return matches
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if query.lower() in text.lower():
                matches.append(str(path.relative_to(self.root)))
                if len(matches) >= max_results:
                    break
        return matches
