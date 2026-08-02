# Status Codes

| Status | Meaning |
| --- | --- |
| `CAPTURED` | Source material has been recorded but not fully classified. |
| `TRIAGED` | The likely route, risks, and next action are identified. |
| `DRAFT` | A record exists but has not passed its required gate. |
| `READY` | The record is complete enough for the named next stage. |
| `IN_PROGRESS` | Work is underway outside the creating agent. |
| `UNDER_REVIEW` | The output is waiting for quality or human review. |
| `ACCEPTED` | A human or authorized gate accepted the output. |
| `HELD` | Work must not advance until a named blocker is resolved. |
| `REJECTED` | The proposed object or action will not advance. |
| `SUPERSEDED` | A newer accepted record replaced this version. |
| `ARCHIVED` | Retained for history but not active. |

Status describes state, not permission. An `ACCEPTED` draft can still require an `ACTION` gate before publication or external execution.

