# ADR-0001: Domain-agnostic eval harness, 3D suite first

- Status: Proposed
- Spec: `specs/001-agent-eval-harness`

## Context

The harness measures whether an agent can be trusted when it uses a deterministic validator. The same pattern applies to other validators, such as the playable ad validator, but only the 3D validator lives in this repository today.

## Decision

Keep the runner, graders, results and gate independent of the 3D domain. The 3D suite is the first and only suite in this change.

## Consequences

- A second domain later needs a suite and a tool adapter, not a rewrite.
- Slightly more structure now than a 3D-only script.

## Alternatives discarded

- 3D-only code: faster now, a rewrite later.
