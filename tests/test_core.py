import json
import unittest
from pathlib import Path

from public_agent_system import AGENTS, new_envelope, validate_envelope


ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_registry_contains_exactly_twelve_unique_agents(self):
        self.assertEqual(12, len(AGENTS))
        self.assertEqual(12, len({agent["id"] for agent in AGENTS}))

    def test_public_registry_file_matches_code_registry(self):
        registry = json.loads((ROOT / "shared/agent-registry.json").read_text(encoding="utf-8"))
        file_pairs = [(agent["id"], agent["name"]) for agent in registry["agents"]]
        code_pairs = [(agent["id"], agent["name"]) for agent in AGENTS]
        self.assertEqual(code_pairs, file_pairs)


class EnvelopeTests(unittest.TestCase):
    def test_sample_handoff_is_valid(self):
        envelope = json.loads((ROOT / "examples/sample-handoff.json").read_text(encoding="utf-8"))
        result = validate_envelope(envelope)
        self.assertTrue(result.valid, result.errors)

    def test_missing_field_is_invalid(self):
        envelope = new_envelope("002", "003", "Define a fictional task", "One work order")
        del envelope["purpose"]
        result = validate_envelope(envelope)
        self.assertFalse(result.valid)
        self.assertTrue(any("Missing fields" in error for error in result.errors))

    def test_review_gate_requires_human_decision(self):
        envelope = new_envelope("002", "003", "Define a fictional task", "One work order")
        envelope["human_decision"]["required"] = False
        envelope["human_decision"]["status"] = "NOT_REQUIRED"
        result = validate_envelope(envelope)
        self.assertFalse(result.valid)
        self.assertTrue(any("requires human_decision.required=true" in error for error in result.errors))

    def test_blocked_gate_cannot_be_approved(self):
        envelope = new_envelope("003", "004", "Review a blocked action", "One review", gate="BLOCKED")
        envelope["human_decision"]["status"] = "APPROVED"
        result = validate_envelope(envelope)
        self.assertFalse(result.valid)
        self.assertTrue(any("BLOCKED" in error for error in result.errors))

    def test_invalid_transition_is_rejected(self):
        envelope = new_envelope("002", "011", "Skip required stages", "Public copy")
        result = validate_envelope(envelope)
        self.assertFalse(result.valid)
        self.assertTrue(any("Transition" in error for error in result.errors))


if __name__ == "__main__":
    unittest.main()
