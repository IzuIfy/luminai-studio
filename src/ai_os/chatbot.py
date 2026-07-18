"""A chatbot that can use a model provider and remember simple facts."""

from __future__ import annotations

import json
from pathlib import Path

from ai_os.automation import DesktopAutomation
from ai_os.providers import ApiModelProvider, ModelProvider, RuleBasedProvider
from ai_os.tools import FileSearchTool, ReminderManager


class SimpleChatbot:
    def __init__(self, provider: ModelProvider | None = None, memory_path: str | None = None) -> None:
        self.provider = provider or ApiModelProvider()
        self.memory_path = Path(memory_path or Path(__file__).resolve().parents[2] / "memory.json")
        self.memory: dict[str, str] = {}
        self.notes: list[str] = []
        self.conversation: list[dict[str, str]] = []
        self.profile: dict[str, str] = {}
        self.tasks: list[dict[str, str]] = []
        self.reminders = ReminderManager()
        self.file_search = FileSearchTool()
        self.automation = DesktopAutomation()
        self._load_memory()

    def _load_memory(self) -> None:
        if not self.memory_path.exists():
            return
        try:
            data = json.loads(self.memory_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        self.memory = data.get("memory", {})
        self.notes = data.get("notes", [])
        self.conversation = data.get("conversation", [])
        self.profile = data.get("profile", {})
        self.tasks = data.get("tasks", [])

    def _save_memory(self) -> None:
        payload = {
            "memory": self.memory,
            "notes": self.notes,
            "conversation": self.conversation,
            "profile": self.profile,
            "tasks": self.tasks,
        }
        self.memory_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _extract_fact(self, text: str) -> tuple[str, str] | None:
        if "my name is" in text:
            name = text.split("my name is", 1)[1].strip().rstrip(".")
            return "name", name
        if "my favorite" in text and "is" in text:
            key, value = text.split("my favorite", 1)[1].split("is", 1)
            return key.strip(), value.strip().rstrip(".")
        if "note that" in text:
            note = text.split("note that", 1)[1].strip().rstrip(".")
            return "note", note
        if "note:" in text:
            note = text.split("note:", 1)[1].strip().rstrip(".")
            return "note", note
        if "i like" in text:
            preference = text.split("i like", 1)[1].strip().rstrip(".")
            return "preference", preference
        if "i prefer" in text:
            preference = text.split("i prefer", 1)[1].strip().rstrip(".")
            return "preference", preference
        if "favorite color" in text and "is" in text:
            color = text.split("is", 1)[1].strip().rstrip(".")
            return "favorite color", color
        return None

    def chat(self, message: str) -> str:
        text = message.strip()
        lowered = text.lower()

        if self._extract_fact(lowered):
            key, value = self._extract_fact(lowered)
            assert key is not None and value is not None
            if key == "note":
                self.notes.append(value)
                self._save_memory()
                return f"I saved your note: {value}"
            self.memory[key] = value
            self.profile[key] = value
            self._save_memory()
            return f"I will remember that {key} is {value}."

        if "what do you remember" in lowered or "remember anything" in lowered:
            if not self.memory and not self.notes and not self.profile:
                return "I do not remember anything yet."
            parts = [f"{k}: {v}" for k, v in self.memory.items()]
            if self.profile:
                parts.extend(f"profile {k}: {v}" for k, v in self.profile.items())
            if self.notes:
                parts.append("notes: " + ", ".join(self.notes))
            return "I remember: " + "; ".join(parts) + "."

        if "history" in lowered or "previous conversation" in lowered:
            if not self.conversation:
                return "There is no previous conversation saved yet."
            summary = "; ".join(f"{entry['role']}: {entry['message']}" for entry in self.conversation[-5:])
            return f"Recent history: {summary}."

        if lowered.startswith("task:"):
            task_text = lowered.split(":", 1)[1].strip()
            self.tasks.append({"task": task_text, "status": "pending"})
            self._save_memory()
            return f"I added a task: {task_text}"

        if "show tasks" in lowered or "my tasks" in lowered:
            if not self.tasks:
                return "You do not have any tasks yet."
            items = "; ".join(f"{item['task']} ({item['status']})" for item in self.tasks)
            return f"Your tasks: {items}."

        if lowered.startswith("remind") or lowered.startswith("reminder"):
            reminder_text = text.split(":", 1)[1].strip() if ":" in text else text.replace("remind", "", 1).strip()
            return self.reminders.add(reminder_text)

        if "show reminders" in lowered or "my reminders" in lowered:
            reminders = self.reminders.list()
            if not reminders:
                return "You do not have any reminders yet."
            return "Reminders: " + "; ".join(item["text"] for item in reminders) + "."

        if lowered.startswith("search "):
            query = text[7:].strip()
            results = self.file_search.search(query)
            if not results:
                return f"No files matched '{query}'."
            return "Matches: " + "; ".join(results) + "."

        if lowered.startswith("plan"):
            plan = text.split(":", 1)[1].strip() if ":" in text else text.replace("plan", "", 1).strip()
            self.tasks.append({"task": plan, "status": "planned"})
            self._save_memory()
            return f"I planned: {plan}"

        if lowered.startswith("open "):
            path = text[5:].strip()
            return self.automation.open_file(path)

        if lowered.startswith("summarize "):
            target = text[10:].strip()
            candidate = (self.file_search.root / target).resolve()
            if candidate.exists() and candidate.is_file():
                try:
                    content = candidate.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    return f"Could not read {target}."
                return self.automation.summarize_text(content)
            return f"I can summarize files if you provide a path inside the workspace."

        self.conversation.append({"role": "user", "message": text})
        if self.provider:
            response = self.provider.generate(text)
        else:
            response = RuleBasedProvider().generate(text)
        self.conversation.append({"role": "assistant", "message": response})
        self._save_memory()
        return response
