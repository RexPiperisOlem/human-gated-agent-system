"""Envelope creation and validation with no network or model dependency."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

from .registry import AGENTS_BY_ID

STATUSES = {
    "CAPTURED",
    "TRIAGED",
    "DRAFT",
    "READY",
    "IN_PROGRESS",
    "UNDER_REVIEW",
    "ACCEPTED",
    "HELD",
    "REJECTED",
    "SUPERSEDED",
    "ARCHIVED",
}
GATES = {"INTERNAL", "REVIEW", "ACTION", "BLOCKED"}
DECISIONS = {"PENDING", "APPROVED", "REJECTED", "NOT_REQUIRED"}
REQUIRED_FIELDS = {
    "record_id",
    "created_at",
    "source_agent",
    "target_agent",
    "status",
    "gate",
    "purpose",
    "inputs",
    "output_contract",
    "risks",
    "human_decision",
    "provenance",
    "payload",
}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: Any) -> bool:
    if not _nonempty_string(value):
        return False
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return True


def validate_envelope(envelope: Mapping[str, Any]) -> ValidationResult:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(envelope))
    if missing:
        errors.append("Missing fields: " + ", ".join(missing))

    source = envelope.get("source_agent")
    target = envelope.get("target_agent")
    if source not in AGENTS_BY_ID:
        errors.append(f"Unknown source_agent: {source!r}")
    if target not in AGENTS_BY_ID:
        errors.append(f"Unknown target_agent: {target!r}")
    if source == target and source in AGENTS_BY_ID:
        errors.append("source_agent and target_agent must differ")
    if source in AGENTS_BY_ID and target in AGENTS_BY_ID:
        if target not in AGENTS_BY_ID[source]["targets"]:
            errors.append(f"Transition {source} -> {target} is not in the public registry")

    if envelope.get("status") not in STATUSES:
        errors.append(f"Invalid status: {envelope.get('status')!r}")
    gate = envelope.get("gate")
    if gate not in GATES:
        errors.append(f"Invalid gate: {gate!r}")
    if not _nonempty_string(envelope.get("record_id")):
        errors.append("record_id must be a non-empty string")
    if not _valid_timestamp(envelope.get("created_at")):
        errors.append("created_at must be an ISO 8601 timestamp")
    if not _nonempty_string(envelope.get("purpose")):
        errors.append("purpose must be a non-empty string")

    inputs = envelope.get("inputs")
    if not isinstance(inputs, list):
        errors.append("inputs must be a list")
    else:
        for index, item in enumerate(inputs):
            if not isinstance(item, Mapping):
                errors.append(f"inputs[{index}] must be an object")
                continue
            if not _nonempty_string(item.get("label")):
                errors.append(f"inputs[{index}].label must be a non-empty string")
            if not _nonempty_string(item.get("reference")):
                errors.append(f"inputs[{index}].reference must be a non-empty string")
            if not isinstance(item.get("required"), bool):
                errors.append(f"inputs[{index}].required must be boolean")

    contract = envelope.get("output_contract")
    if not isinstance(contract, Mapping):
        errors.append("output_contract must be an object")
    else:
        if not _nonempty_string(contract.get("primary_deliverable")):
            errors.append("output_contract.primary_deliverable must be a non-empty string")
        criteria = contract.get("acceptance_criteria")
        if not isinstance(criteria, list) or not all(_nonempty_string(item) for item in criteria):
            errors.append("output_contract.acceptance_criteria must be a list of non-empty strings")

    if not isinstance(envelope.get("risks"), list):
        errors.append("risks must be a list")
    if not isinstance(envelope.get("provenance"), list):
        errors.append("provenance must be a list")
    if not isinstance(envelope.get("payload"), Mapping):
        errors.append("payload must be an object")

    decision = envelope.get("human_decision")
    if not isinstance(decision, Mapping):
        errors.append("human_decision must be an object")
    else:
        required = decision.get("required")
        decision_status = decision.get("status")
        if not isinstance(required, bool):
            errors.append("human_decision.required must be boolean")
        if decision_status not in DECISIONS:
            errors.append(f"Invalid human_decision.status: {decision_status!r}")
        if not _nonempty_string(decision.get("owner_role")):
            errors.append("human_decision.owner_role must be a non-empty string")
        if gate in {"REVIEW", "ACTION", "BLOCKED"} and required is not True:
            errors.append(f"Gate {gate} requires human_decision.required=true")
        if required is False and decision_status != "NOT_REQUIRED":
            errors.append("A non-required decision must use status NOT_REQUIRED")
        if gate == "BLOCKED" and decision_status == "APPROVED":
            errors.append("A BLOCKED envelope cannot use human decision status APPROVED")

    return ValidationResult(tuple(errors))


def new_envelope(
    source_agent: str,
    target_agent: str,
    purpose: str,
    primary_deliverable: str,
    gate: str = "REVIEW",
) -> dict[str, Any]:
    gate = gate.upper()
    decision_required = gate != "INTERNAL"
    return {
        "record_id": f"HANDOFF-{uuid4().hex[:12].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_agent": source_agent,
        "target_agent": target_agent,
        "status": "DRAFT",
        "gate": gate,
        "purpose": purpose,
        "inputs": [],
        "output_contract": {
            "primary_deliverable": primary_deliverable,
            "acceptance_criteria": [],
        },
        "risks": [],
        "human_decision": {
            "required": decision_required,
            "status": "PENDING" if decision_required else "NOT_REQUIRED",
            "owner_role": "system owner",
            "decision_note": "",
        },
        "provenance": [],
        "payload": {},
    }

