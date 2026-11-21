# Spec 001: Agent eval harness

- Status: Draft
- Owner: Aitor Nain (`naindev`)
- Decisions: ADR-0001 to ADR-0004 (all `Proposed`)
- Package: `src/nain_mcp_validator_evals/` (new), report page under `site/evals/`

## Why

The server proves that a mesh is or is not valid. It does not yet prove that an AI agent that uses the server behaves better than one that does not. This spec adds a harness that measures it, with the validator itself as the oracle, so no LLM judge is needed.

The headline metric is the **hallucinated pass**: the agent says a mesh is conformant while the validator says it is not.

## Goal

A reproducible run that executes the same task suite against two arms (agent without tools, agent with the MCP server), grades each task deterministically, stores traces, publishes a results page and fails CI when the hallucinated-pass rate regresses.

## Requirements (EARS)

- **REQ-EVAL-01 Task suite.** When the suite is loaded, the harness shall build each task's mesh from code with a fixed seed and declare its expected verdict and, for a defective mesh, the check id (C1 to C10) it violates. The repository shall contain no binary mesh files.
- **REQ-EVAL-02 Ground-truth self-check.** When the suite is built, the harness shall run the server's own domain checks on every generated mesh and fail the build if a verdict or check id differs from the task declaration.
- **REQ-EVAL-03 Runner.** When a run starts, the harness shall launch the MCP server as a subprocess over stdio and drive an agent loop with a configurable model backend and a maximum number of steps.
- **REQ-EVAL-04 Arms.** The harness shall run every task in two arms: `no-tools` (the agent receives the mesh as text and no tools) and `mcp-tools` (the agent may call the three server tools).
- **REQ-EVAL-05 Traces.** When a task finishes, the harness shall write one JSONL trace with every step: tool name, arguments, result, latency and token counts when the backend reports them.
- **REQ-EVAL-06 Graders.** The harness shall grade each task deterministically on: `verdict_correct`, `hallucinated_pass`, `tool_call_valid`, step count and latency. A grader shall never call a model.
- **REQ-EVAL-07 Failure is data.** If a model call errors or times out, the harness shall record the task as failed with the reason and continue the run.
- **REQ-EVAL-08 Results file.** The harness shall write one aggregated results JSON with no timestamps, paths or host names, and print its SHA-256 so two runs of the same recorded traces can be compared byte for byte.
- **REQ-EVAL-09 Regression gate.** When the gate runs against a committed baseline, the harness shall fail if the hallucinated-pass rate of the `mcp-tools` arm is higher than the baseline, or if verdict accuracy falls by more than the tolerance declared in the baseline file.
- **REQ-EVAL-10 Report page.** When the site is built, the generator shall render the results table and a trace viewer from the results JSON, shall make no network call, and shall fail if the JSON is invalid.
- **REQ-EVAL-11 Offline by default.** The harness and its tests shall run without network access. Model calls shall go only to the configured local endpoint. A hosted backend shall be used only when its key is present in an environment variable.

## Non-functional

- Python 3.11 or later. Standard library first. A new dependency needs an ADR.
- The unit tests use a scripted fake backend. CI never calls a real model.
- Live runs with a real model are manual and their results are committed as a baseline.

## Out of scope

- Fine-tuning, RAG and the playable ad domain (separate specs after this one).
- Remote (HTTP) transport for the server.
- Any client asset or private repository content.

## Edge cases

- A model that never calls a tool in the `mcp-tools` arm: graded as is, no retry.
- A tool call with arguments that break the JSON Schema: counted in `tool_call_valid`, the server error goes back to the agent.
- A defect-free mesh that the agent calls defective: counted in `verdict_correct`, not in `hallucinated_pass`.

## Acceptance criteria

1. `npm`-free: one command builds the suite, runs the fake backend and prints the results SHA-256.
2. The self-check fails when a task declaration is wrong (tested).
3. The gate fails on a worse baseline and passes on an equal one (tested).
4. `mcp.naindev.com/evals/` shows both arms, with real numbers from a recorded live run.

## Open items

See `docs/11-open-questions.md`.
