# Human-Gated Agent System

Public reference edition, version 1.0.

This repository contains a document-first operating system for coordinating twelve narrow artificial-intelligence agents without giving any agent final authority over consequential actions. Each agent has one job, a defined input, a structured output, explicit stop conditions, and a human approval gate.

The system is model-agnostic. The prompts can be used with a hosted model, a local model, or a human operator. The small Python utility validates handoff records; it does not call a model, publish content, modify external systems, spend money, or delete files.

## The twelve agents

| Agent | Public role | Primary output |
| --- | --- | --- |
| 001 | System Orchestrator | Dispatch record |
| 002 | Intake and Triage | Intake card |
| 003 | Work Order Designer | Executable work order |
| 004 | Quality and Evidence Gate | Review decision and repair list |
| 005 | Index and Provenance Recorder | Index update packet |
| 006 | Controlled Change Agent | Patch proposal |
| 007 | Collection Intake | Object record |
| 008 | Digital Capture Control | Capture record |
| 009 | Preservation Planning | Storage and handling plan |
| 010 | Retention and Release Gate | Controlled disposition decision |
| 011 | Public Description Builder | Fact-grounded public copy draft |
| 012 | Voice and Style Router | Routed, style-checked text |

Agents 001-006 form the universal control loop. Agents 007-011 form an optional collection-management branch. Agent 012 is a cross-cutting service used whenever output style or public/private boundaries matter.

## Why this architecture exists

- Raw material is captured before it becomes work.
- Work is defined before it is executed.
- Output is checked against evidence and acceptance criteria.
- Accepted artifacts remain findable and traceable.
- System rules change through reviewable patches, not silent rewrites.
- External, destructive, financial, privacy-sensitive, or public actions stop for a human decision.

## Quick start

1. Read [the architecture](docs/architecture.md) and [governance rules](docs/governance-and-gates.md).
2. Start with the prompt in `agents/001-system-orchestrator/prompt.md`.
3. Pass work between agents using `shared/templates/handoff-envelope.json`.
4. Validate a handoff record:

   ```bash
   python -m public_agent_system validate examples/sample-handoff.json
   ```

5. Run the repository checks:

   ```bash
   python scripts/repository_check.py
   python -m unittest discover -s tests -v
   ```

For a complete walkthrough, see [Quick Start](docs/quickstart.md). Before publishing, complete the [Publication Checklist](docs/publication-checklist.md).

## Gate levels

| Gate | Meaning |
| --- | --- |
| `INTERNAL` | Read, classify, draft, or inspect without changing an external system. |
| `REVIEW` | A human must confirm the record before downstream work proceeds. |
| `ACTION` | A human must explicitly authorize the exact external, destructive, financial, or public action. |
| `BLOCKED` | This reference system must not automate the action. |

An approval is specific to one action and one target. Approval to draft is not approval to publish. Approval to recommend a file move is not approval to move the file.

## What is deliberately absent

This is a clean public rebuild. It contains no private source documents, brand doctrine, personal style profiles, production records, customer or collaborator data, real collection records, private images, live-platform configuration, credentials, or original test material. See [Sanitization Boundary](docs/sanitization-boundary.md).

## Repository status

The public reference system is complete enough to study, adapt privately, and test with fictional inputs. It is not a turnkey autonomous operator. Before using it in a real organization, define your own authority roles, risk policy, data-retention rules, legal obligations, and domain-specific safety controls.

## License status

This repository is source-available for inspection under the included restrictive notice. No permission to copy, modify, distribute, or sell is granted unless the repository owner replaces `LICENSE` with a chosen license.
