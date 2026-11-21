# ADR-0004: Publish the results at `/evals/` in the same repository

- Status: Proposed
- Spec: `specs/001-agent-eval-harness`

## Context

`mcp.naindev.com` already serves the project page from this repository through GitHub Pages with a custom domain.

## Decision

Add the results page and trace viewer under `site/evals/`, so it is served at `mcp.naindev.com/evals/`. No new repository and no new subdomain.

## Consequences

- One deployment, one domain, and the data stays next to the server it measures.
- If the harness later grows into its own project, it can move to a one-level subdomain with its own Pages custom domain.

## Alternatives discarded

- A new repository and subdomain: more setup for no benefit at this size.
