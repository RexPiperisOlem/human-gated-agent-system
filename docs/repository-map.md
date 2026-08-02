# Repository Map

| Path | Purpose |
| --- | --- |
| `agents/` | Public operating contract, prompt, and record template for each agent. |
| `docs/` | Architecture, governance, quick start, sanitization, and customization guidance. |
| `shared/` | Common status codes, risk codes, schemas, templates, and example style profiles. |
| `examples/` | Fictional inputs and handoff records. |
| `src/public_agent_system/` | Local validation and registry utility. |
| `tests/` | Standard-library unit tests. |
| `scripts/` | Repository safety and completeness checks. |
| `.github/` | Continuous integration and contribution templates. |

Each agent folder has the same three-file shape:

- `agent.md`: mission, boundaries, gates, failure modes, and handoffs.
- `prompt.md`: generic paste-ready operating prompt.
- `record-template.md`: structured output contract.

