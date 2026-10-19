import json

from nain_mcp_validator.server import handle_json_rpc


def test_mcp_initialize() -> None:
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {},
    }
    resp = handle_json_rpc(req)
    assert resp is not None
    assert resp["id"] == 1
    assert resp["result"]["serverInfo"]["name"] == "nain-mcp-validator"


def test_mcp_tools_list() -> None:
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
    }
    resp = handle_json_rpc(req)
    assert resp is not None
    tools = resp["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "validate_mesh_invariants" in tool_names
    assert "verify_content_digest" in tool_names
    assert "generate_conformance_report" in tool_names


def test_mcp_tools_call_validate_mesh() -> None:
    req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "validate_mesh_invariants",
            "arguments": {
                "vertices": [
                    [1.0, 1.0, 1.0],
                    [-1.0, -1.0, 1.0],
                    [-1.0, 1.0, -1.0],
                    [1.0, -1.0, -1.0],
                ],
                "faces": [
                    [0, 1, 2],
                    [0, 3, 1],
                    [0, 2, 3],
                    [1, 3, 2],
                ],
            },
        },
    }
    resp = handle_json_rpc(req)
    assert resp is not None
    assert "result" in resp
    content = json.loads(resp["result"]["content"][0]["text"])
    assert content["is_conforming"] is True
