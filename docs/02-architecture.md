# System Architecture: nain-mcp-validator

## 1. Architectural Blueprint

```mermaid
flowchart LR
    classDef client fill:#0284c7,stroke:#0369a1,color:#fff;
    classDef mcp fill:#0047AB,stroke:#38bdf8,stroke-width:2px,color:#fff;
    classDef domain fill:#059669,stroke:#34d399,color:#fff;

    client[AI Agent / Assistant<br/>Claude / Antigravity / Cursor]:::client
    transport[Stdio Transport<br/>JSON-RPC 2.0 Loop]:::mcp
    dispatcher[Tool Dispatcher]:::mcp
    checks[Checks Engine C1-C10<br/>Quantum Threshold 10⁻¹² m²]:::domain
    digest[Digest Verification<br/>SHA-256 Digest Engine]:::domain
    reporter[Conformance Reporter<br/>Fail-Closed Markdown]:::domain

    client -->|stdin: tools/call| transport
    transport --> dispatcher
    dispatcher -->|validate_mesh_invariants| checks
    dispatcher -->|verify_content_digest| digest
    dispatcher -->|generate_conformance_report| reporter
    dispatcher -->|stdout: result| transport
    transport -->|stdout: JSON-RPC response| client
```

## 2. Directory Layout

```text
nain-mcp-validator/
├── docs/                # Spec-driven numbered lifecycle documentation
├── src/
│   └── nain_mcp_validator/
│       ├── __init__.py
│       ├── server.py    # MCP stdio JSON-RPC server loop
│       └── domain/
│           ├── checks.py   # Deterministic topological checks C1 to C10
│           ├── digest.py   # Content-addressing SHA-256 verifier
│           └── reporter.py # Markdown audit reporter
├── tests/
│   ├── test_checks.py
│   ├── test_digest.py
│   └── test_server.py
├── pyproject.toml
└── README.md
```
