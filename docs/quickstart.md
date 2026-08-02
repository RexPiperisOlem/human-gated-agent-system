# Quick Start

This walkthrough uses a fictional task: create a short public guide for a neighborhood tool-sharing event.

## 1. Dispatch

Use `agents/001-system-orchestrator/prompt.md`. The orchestrator should route the raw request to Agent 002 because the task is still loose and public-facing.

Expected dispatch fields:

- route: `002`
- likely later route: `003`, then `012`, then `004`
- gate: `REVIEW`
- prohibited action: no publication or external sending

## 2. Triage

Use `agents/002-intake-and-triage/prompt.md`. The output should capture the intended audience, desired artifact, known source material, risks, and no more than two immediate next actions.

## 3. Define the work

Use `agents/003-work-order-designer/prompt.md`. The work order should name one primary deliverable, such as `A two-page public event guide in Markdown`, and include testable acceptance criteria.

## 4. Draft with style control

If voice matters, pass the work order through Agent 012 using a neutral public profile from `shared/style-profiles.example.json`. Keep personal or brand profiles outside the repository.

## 5. Review

Use Agent 004 to compare the draft with the work order. A valid review separates blocking defects from optional improvements and returns one decision code.

## 6. Record

After human acceptance, Agent 005 creates an index entry and provenance chain. It may recommend a location, but it does not move files.

## 7. Improve the system only when evidence supports it

If the same failure repeats, Agent 006 may propose a small, reviewable patch. The active rule does not change until a human approves the patch.

## Local validation utility

From the repository root:

```bash
PYTHONPATH=src python -m public_agent_system list
PYTHONPATH=src python -m public_agent_system validate examples/sample-handoff.json
PYTHONPATH=src python -m public_agent_system show 004
```

The utility validates structure. It does not decide whether the content is true, safe, lawful, or approved.

