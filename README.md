# nain-mcp-validator

> Standalone Model Context Protocol (MCP) server providing deterministic 3D asset validation (checks C1-C10), content-addressed artifact verification (SHA-256), and fail-closed conformance reporting for AI engineering agents.

[![Language: English](https://img.shields.io/badge/Language-English-blue.svg)](#)
[![Versión en Español](https://img.shields.io/badge/Versión-Español-red.svg)](README.es.md)
[![Protocol](https://img.shields.io/badge/MCP-2024--11--05-0047AB)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB)](https://www.python.org/)
[![Validation](https://img.shields.io/badge/Checks-C1_to_C10-22c55e)](docs/01-requirements.md)
[![License](https://img.shields.io/badge/License-MIT-gray)](LICENSE)

---

## 1. Overview

`nain-mcp-validator` solves the reliability gap when AI agents generate CAD geometry, meshes, or engineering specifications. Instead of relying on probabilistic text inspection, it equips agents with deterministic validation tools:

- `validate_mesh_invariants`: Topological validation enforcing watertight closure, 2-manifold boundaries, outward normal consistency, and the quantum sliver threshold ($10^{-12}\text{ m}^2$).
- `verify_content_digest`: Cryptographic verification of SHA-256 content hashes.
- `generate_conformance_report`: Produces standardized markdown conformance audits with a fail-closed verdict.

## 2. Quickstart & Testing

```bash
# Run pytest verification suite
pytest -v
```

## 3. Integration with AI Clients

Add the server to your Claude Desktop or Cursor configuration:

```json
{
  "mcpServers": {
    "nain-validator": {
      "command": "python",
      "args": ["-m", "nain_mcp_validator.server"],
      "cwd": "/path/to/nain-mcp-validator"
    }
  }
}
```

---

**Author**: Aitor Nain Mendoza Vallejo  
**Standards**: [NainDev Engineering Handbook](https://github.com/Nain9Dev/engineering-handbook)
