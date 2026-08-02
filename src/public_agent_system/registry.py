"""Canonical public agent registry used by the local validator."""

from __future__ import annotations

AGENTS = (
    {"id": "001", "name": "System Orchestrator", "output": "Dispatch record", "targets": ("002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012")},
    {"id": "002", "name": "Intake and Triage", "output": "Intake card", "targets": ("001", "003", "005")},
    {"id": "003", "name": "Work Order Designer", "output": "Executable work order", "targets": ("001", "004", "007", "008", "009", "010", "011", "012")},
    {"id": "004", "name": "Quality and Evidence Gate", "output": "Review decision and repair list", "targets": ("001", "003", "005", "012")},
    {"id": "005", "name": "Index and Provenance Recorder", "output": "Index update packet", "targets": ("001", "006")},
    {"id": "006", "name": "Controlled Change Agent", "output": "Patch proposal", "targets": ("001", "004", "005")},
    {"id": "007", "name": "Collection Intake", "output": "Object record", "targets": ("001", "004", "005", "008")},
    {"id": "008", "name": "Digital Capture Control", "output": "Capture record", "targets": ("001", "004", "005", "009")},
    {"id": "009", "name": "Preservation Planning", "output": "Storage and handling plan", "targets": ("001", "004", "005", "010")},
    {"id": "010", "name": "Retention and Release Gate", "output": "Controlled disposition decision", "targets": ("001", "004", "005", "011")},
    {"id": "011", "name": "Public Description Builder", "output": "Fact-grounded public copy draft", "targets": ("001", "004", "005", "012")},
    {"id": "012", "name": "Voice and Style Router", "output": "Routed and style-checked text", "targets": ("001", "003", "004", "005")},
)

AGENTS_BY_ID = {agent["id"]: agent for agent in AGENTS}

