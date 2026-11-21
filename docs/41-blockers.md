# Blockers

| ID | What | Where to get it | Variable | Unblocks | How to verify |
| :--- | :--- | :--- | :--- | :--- | :--- |
| B-001 | Owner approval of ADR-0001 to ADR-0004 | Owner | none | Every task | Status changed to `Approved` |
| B-002 | A local model with tool calling, served by Ollama | Already installed on the workstation, model to be chosen (Q-001) | `EVAL_OLLAMA_MODEL` | T-015 | `ollama list` shows it and a one-tool test call succeeds |
| B-003 | Hosted model key (optional) | Provider account, owner only | `EVAL_HOSTED_API_KEY` | Hosted comparison only | Not needed for the first release |

Nothing else is external: GitHub Pages and the `mcp.naindev.com` custom domain already exist.
