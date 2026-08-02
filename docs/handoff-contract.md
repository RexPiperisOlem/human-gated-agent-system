# Handoff Contract

Every handoff uses one envelope. The envelope identifies the source, target, purpose, output contract, gate, risks, human decision, and provenance.

## Required fields

| Field | Requirement |
| --- | --- |
| `record_id` | Stable, unique identifier for the handoff. |
| `created_at` | International Organization for Standardization (ISO) 8601 timestamp. |
| `source_agent` | Three-digit source agent identifier. |
| `target_agent` | Three-digit target agent identifier. |
| `status` | Approved system status code. |
| `gate` | `INTERNAL`, `REVIEW`, `ACTION`, or `BLOCKED`. |
| `purpose` | One-sentence reason for the handoff. |
| `inputs` | References to supplied source material. |
| `output_contract` | One primary deliverable and acceptance criteria. |
| `risks` | Material risk flags or an empty list. |
| `human_decision` | Whether review is required and its current status. |
| `provenance` | Trace back to the request, intake, work order, or source. |
| `payload` | Agent-specific structured data. |

## Clean handoff rules

- The target agent should not need to infer the main deliverable.
- Sensitive source content should be referenced, not duplicated, when possible.
- Missing evidence must be visible.
- `ACTION` and `BLOCKED` envelopes cannot claim executed status through the reference utility.
- One envelope should represent one primary transition.

See `shared/schemas/handoff-envelope.schema.json` and `shared/templates/handoff-envelope.json`.

