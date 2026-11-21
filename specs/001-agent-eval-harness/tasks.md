# Tasks: agent eval harness

Labels: `[A]` the agent alone, `[M]` mixed, `[H]` owner only. Each task is under 30 minutes and test first.

Status: nothing started. Blocked on the owner approving this spec and ADR-0001 to ADR-0004.

| ID | Label | Task | Done when |
| :--- | :--- | :--- | :--- |
| T-001 | [A] | Create the `evals` package skeleton and the `Task` dataclass | `pytest tests/evals/test_tasks.py` passes |
| T-002 | [A] | Seeded generator for a clean closed mesh | Same seed gives identical vertices (test) and the domain checks pass it |
| T-003 | [A] | Generators for defects C1 to C5 and C10, one per check | Each mesh fails exactly its declared check (test) |
| T-004 | [A] | Self-check: compare the declaration with the domain checks | Passes on the suite, fails on a deliberately wrong declaration (test) |
| T-005 | [A] | Pure graders: `verdict_correct`, `hallucinated_pass`, `tool_call_valid` | Table tests cover each case in the spec's edge cases |
| T-006 | [A] | Results aggregation, canonical JSON and SHA-256 | Two aggregations of the same traces give the same hash (test) |
| T-007 | [A] | Regression gate against a baseline file | Fails on a worse baseline, passes on an equal one (test) |
| T-008 | [A] | MCP stdio client that spawns the server | Lists tools and calls one against the real server in a test |
| T-009 | [A] | `ModelBackend` protocol and `ScriptedBackend` | A scripted conversation replays deterministically (test) |
| T-010 | [A] | Agent loop, arm `mcp-tools`, with step limit and error capture | Scripted run records a trace and a failed task on a model error (test) |
| T-011 | [A] | Agent loop, arm `no-tools` | Scripted run completes without any tool call (test) |
| T-012 | [A] | JSONL trace writer | Trace round-trips and holds no timestamps in the aggregate (test) |
| T-013 | [A] | CLI: build suite, run, grade, print results hash | One command runs the fake backend end to end |
| T-014 | [A] | `OllamaBackend` over local HTTP | Request shape tested against a stub server, no real model |
| T-015 | [M] | Live run with a local model, commit traces and baseline | Needs the owner to confirm the model and that Ollama is running. Baseline file committed |
| T-016 | [A] | Results page and trace viewer generator | Renders the fixture, fails on invalid JSON (test) |
| T-017 | [A] | CI job for the gate and the page | Pipeline green on the PR |
| T-018 | [A] | Update `docs/10-requirements.md`, `50-traceability.md`, README and changelog | Every REQ-EVAL has a passing test listed |

Handoff notes: write the state of the last finished task here at the end of every session.
