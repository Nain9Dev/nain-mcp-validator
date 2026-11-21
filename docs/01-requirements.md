# Requirements Specification: nain-mcp-validator

## 1. Functional Requirements (EARS)

### REQ-MCP-01: Tool Discovery
- **Statement**: When an MCP client sends a `tools/list` JSON-RPC request, the server shall return tool definitions for `validate_mesh_invariants`, `verify_content_digest`, and `generate_conformance_report` with strict JSON Schema schemas.

### REQ-MCP-02: Deterministic Mesh Invariant Validation
- **Statement**: When an agent invokes `validate_mesh_invariants`, the server shall execute checks C1 through C10:
  - C1: Buffer integrity (no NaN/infinite coordinates or orphan vertices).
  - C2: Degenerate face count using the quantum threshold of $10^{-12}\text{ m}^2$.
  - C3: 2-Manifold topology (each edge shared by at most 2 faces).
  - C4: Watertight closure (zero boundary edges for closed solids).
  - C5: Outward normal and winding consistency.
  - C10: Euler-Poincaré invariant ($\chi = 2 \cdot (\text{bodies} - \text{genus})$).

### REQ-MCP-03: Content Digest Verification
- **Statement**: When an agent invokes `verify_content_digest`, the server shall compute the SHA-256 hash of the input data and compare it against the expected hash, failing closed on mismatch.

### REQ-MCP-04: Conformance Report Generation
- **Statement**: When an agent invokes `generate_conformance_report`, the server shall format the check results into a standardized Markdown audit summary with an explicit pass/fail gate.

### REQ-SEO-01: Project Page Discoverability
- **Statement**: When a crawler or AI engine fetches the public project page, the site shall expose a single canonical URL, a 70-160 character description, Open Graph and Twitter metadata, `SoftwareApplication` JSON-LD, `robots.txt`, `sitemap.xml` and `llms.txt` at the site root.
- **Verification**: `tests/test_site_seo.py`.

### REQ-PWA-01: Installable Project Page
- **Statement**: When a visitor opens the public project page in Android Chrome or iOS Safari, the site shall publish `manifest.webmanifest` and PNG install icons at the site root and link them from the page with the iOS head tags, so the page installs as a standalone app named `Nain MCP`. The site shall register no service worker.
- **Verification**: `tests/test_site_install.py`; spec in `specs/next-pwa-install/spec.md`.

### REQ-PKG-01: Console Script
- **Statement**: When the package is installed, it shall provide the console script `nain-mcp-validator` that starts the stdio JSON-RPC server.
- **Verification**: `tests/test_packaging.py`; run through `uvx --from . nain-mcp-validator`.

### REQ-PKG-02: MCP Registry Descriptor
- **Statement**: The repository shall carry a `server.json` whose name is `io.github.Nain9Dev/nain-mcp-validator` and whose version, repository, PyPI package and stdio transport match `pyproject.toml`.
- **Verification**: `tests/test_packaging.py`.

### REQ-PKG-03: PyPI Ownership Marker
- **Statement**: The README shall contain the line `mcp-name: io.github.Nain9Dev/nain-mcp-validator`, which the official registry reads to verify a PyPI package.
- **Verification**: `tests/test_packaging.py`.

## 2. Non-Functional Requirements

- **NFR-01: Protocol Compliance**: JSON-RPC 2.0 over stdio with UTF-8 encoding.
- **NFR-02: Zero Network Access**: Operates offline without external network calls or cloud dependencies.
