#!/usr/bin/env python3
"""Check public repository completeness and common leakage indicators."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".py", ".json", ".toml", ".yml", ".yaml", ".txt"}
FORBIDDEN_BINARY_SUFFIXES = {".docx", ".xlsx", ".zip", ".7z", ".rar", ".tif", ".tiff", ".psd"}
REQUIRED_ROOT_FILES = {
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "pyproject.toml",
}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Amazon access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "generic secret assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    "Windows user path": re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+"),
    "macOS user path": re.compile("/" + r"Users/[^/\s]+"),
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check() -> list[str]:
    errors: list[str] = []
    present = {path.name for path in ROOT.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_ROOT_FILES - present)
    if missing:
        errors.append("Missing root files: " + ", ".join(missing))

    agent_dirs = sorted(path for path in (ROOT / "agents").iterdir() if path.is_dir())
    if len(agent_dirs) != 12:
        errors.append(f"Expected 12 agent directories, found {len(agent_dirs)}")
    directory_ids = [path.name[:3] for path in agent_dirs]
    if directory_ids != [f"{number:03d}" for number in range(1, 13)]:
        errors.append("Agent directories must begin with ordered IDs 001 through 012")
    for agent_dir in agent_dirs:
        for required in ("agent.md", "prompt.md", "record-template.md"):
            if not (agent_dir / required).is_file():
                errors.append(f"Missing {agent_dir.relative_to(ROOT) / required}")

    registry_path = ROOT / "shared/agent-registry.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        ids = [agent["id"] for agent in registry["agents"]]
        if ids != [f"{number:03d}" for number in range(1, 13)]:
            errors.append("Agent registry must contain ordered IDs 001 through 012")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid agent registry: {exc}")

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            errors.append(f"Forbidden source/binary artifact: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", ".gitignore"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Non-UTF-8 text file: {path.relative_to(ROOT)}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Possible {label} in {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".md":
            for target in MARKDOWN_LINK.findall(text):
                target = target.strip().split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (path.parent / target).resolve()
                if not resolved.exists():
                    errors.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")

    return errors


def main() -> int:
    errors = check()
    if errors:
        print("REPOSITORY CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REPOSITORY CHECK PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
