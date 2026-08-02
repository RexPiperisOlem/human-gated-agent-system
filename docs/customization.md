# Customization Guide

## Start with roles, not wording

Keep the twelve public roles stable during the first test. Customize vocabulary, department names, risk flags, and record fields only after a real run exposes a mismatch.

## Define authority roles

Replace the generic `system owner` role with the actual role that can approve classification, public copy, external action, release decisions, and rule changes. Do not use a person's name in public templates.

## Add domain branches

A new specialist branch should define:

- the trigger that routes work into it;
- one narrow agent per meaningful stage;
- the record passed between stages;
- what each agent is forbidden to do;
- the return path to Agent 004 and Agent 005;
- the exact human gate before external action.

## Create private style profiles

Copy `shared/style-profiles.example.json` into an ignored private location. Replace fictional profiles with your own evidence-backed rules. Do not commit personal examples, private writing samples, or confidential brand guidance.

## Add model integration cautiously

The public utility intentionally makes no model calls. If a project adds them:

1. keep credentials outside source control;
2. log model and prompt versions without logging sensitive source content;
3. set input and output size limits;
4. treat model output as untrusted data;
5. require a human gate before external action;
6. add tests for prompt injection, data leakage, and invalid structured output.

