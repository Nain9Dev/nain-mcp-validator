"""REQ-PKG-01 to REQ-PKG-03: the server can be installed and listed in the official MCP Registry."""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
NAME = "io.github.Nain9Dev/nain-mcp-validator"


def _pyproject() -> dict[str, Any]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def test_console_script_starts_the_stdio_server() -> None:
    """REQ-PKG-01: `nain-mcp-validator` is a console script that runs the stdio loop."""
    scripts = _pyproject()["project"]["scripts"]
    assert scripts["nain-mcp-validator"] == "nain_mcp_validator.server:run_server"


def test_server_json_matches_the_package() -> None:
    """REQ-PKG-02: server.json names the same server, version and PyPI package."""
    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    project = _pyproject()["project"]
    assert server["name"] == NAME
    assert server["version"] == project["version"]
    assert server["repository"]["url"] == "https://github.com/Nain9Dev/nain-mcp-validator"
    (package,) = server["packages"]
    assert package["registryType"] == "pypi"
    assert package["identifier"] == project["name"]
    assert package["version"] == project["version"]
    assert package["transport"] == {"type": "stdio"}
    assert len(server["description"]) <= 100


def test_readme_carries_the_pypi_ownership_marker() -> None:
    """REQ-PKG-03: the registry verifies a PyPI package through `mcp-name:` in the README."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"mcp-name: {NAME}" in readme
