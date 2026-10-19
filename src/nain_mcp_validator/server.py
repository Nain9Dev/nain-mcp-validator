from __future__ import annotations

import json
import sys
from typing import Any

from nain_mcp_validator.domain.checks import Point3D, validate_triangular_mesh
from nain_mcp_validator.domain.digest import verify_sha256
from nain_mcp_validator.domain.reporter import generate_markdown_report

TOOLS_DEFINITIONS = [
    {
        "name": "validate_mesh_invariants",
        "description": "Deterministic validation of 3D triangular mesh invariants (checks C1-C10) including watertightness, 2-manifoldness, quantum sliver threshold, and normal winding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "vertices": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                    "description": "List of [x, y, z] coordinate triplets.",
                },
                "faces": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                    "description": "List of [i0, i1, i2] vertex index triplets.",
                },
                "bodies": {
                    "type": "integer",
                    "default": 1,
                    "description": "Expected number of disjoint bodies (default: 1).",
                },
                "genus": {
                    "type": "integer",
                    "default": 0,
                    "description": "Expected genus/through-holes (default: 0).",
                },
            },
            "required": ["vertices", "faces"],
        },
    },
    {
        "name": "verify_content_digest",
        "description": "Cryptographic content-addressing validation ensuring an artifact or specification matches its immutable SHA-256 digest.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "UTF-8 content string to hash and verify.",
                },
                "expected_sha256": {
                    "type": "string",
                    "description": "64-character hexadecimal SHA-256 digest to compare against.",
                },
            },
            "required": ["content", "expected_sha256"],
        },
    },
    {
        "name": "generate_conformance_report",
        "description": "Generates a standardized Markdown dual-contract conformance report from mesh validation results with fail-closed summary.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "asset_name": {
                    "type": "string",
                    "description": "Identifier or filename of the asset.",
                },
                "vertices": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                },
                "faces": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                },
            },
            "required": ["asset_name", "vertices", "faces"],
        },
    },
]

def handle_tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "validate_mesh_invariants":
        raw_verts = arguments.get("vertices", [])
        raw_faces: list[tuple[int, int, int]] = [
            (int(f[0]), int(f[1]), int(f[2])) for f in arguments.get("faces", [])
        ]
        bodies = arguments.get("bodies", 1)
        genus = arguments.get("genus", 0)

        pts = [Point3D(x=float(v[0]), y=float(v[1]), z=float(v[2])) for v in raw_verts]
        result = validate_triangular_mesh(pts, raw_faces, bodies=bodies, genus=genus)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result.model_dump(), indent=2),
                }
            ],
            "isError": not result.is_conforming,
        }

    elif name == "verify_content_digest":
        content = arguments.get("content", "")
        expected_sha256 = arguments.get("expected_sha256", "")
        res = verify_sha256(content, expected_sha256)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(res.model_dump(), indent=2),
                }
            ],
            "isError": not res.is_valid,
        }

    elif name == "generate_conformance_report":
        asset_name = arguments.get("asset_name", "UnknownAsset")
        raw_verts = arguments.get("vertices", [])
        raw_faces = [
            (int(f[0]), int(f[1]), int(f[2])) for f in arguments.get("faces", [])
        ]
        pts = [Point3D(x=float(v[0]), y=float(v[1]), z=float(v[2])) for v in raw_verts]
        result = validate_triangular_mesh(pts, raw_faces)
        report_md = generate_markdown_report(asset_name, result)
        return {
            "content": [
                {
                    "type": "text",
                    "text": report_md,
                }
            ],
            "isError": not result.is_conforming,
        }

    raise ValueError(f"Unknown tool: {name}")

def handle_json_rpc(request: dict[str, Any]) -> dict[str, Any] | None:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                },
                "serverInfo": {
                    "name": "nain-mcp-validator",
                    "version": "0.1.0",
                },
            },
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS_DEFINITIONS,
            },
        }

    elif method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        try:
            call_result = handle_tool_call(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": call_result,
            }
        except Exception as e:  # noqa: BLE001
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": str(e),
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}",
        },
    }

def run_server() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_json_rpc(req)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as err:  # noqa: BLE001
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {err}"},
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_server()
