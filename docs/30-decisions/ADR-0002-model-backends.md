# ADR-0002: Local model by default, hosted backend opt-in

- Status: Proposed
- Spec: `specs/001-agent-eval-harness`

## Context

Runs must be cheap and reproducible, and CI must never depend on a model.

## Decision

- The default backend talks to a local Ollama endpoint on `127.0.0.1`.
- A hosted backend exists behind a `ModelBackend` protocol and is used only when its key is present in an environment variable. The key is never written to a file, trace or result.
- Unit tests use a scripted fake backend. CI never calls a real model.
- The HTTP calls use the standard library, so no new dependency is added.

## Consequences

- Live results depend on the local model and its version. The model name and version are recorded in the results file.
- Hosted comparisons are possible later without a code change in the loop.

## Alternatives discarded

- Hosted only: cost, and results that change without notice.
- A third-party client library: a new dependency for a small request shape.
