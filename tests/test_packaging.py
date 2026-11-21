"""REQ-PKG-01 to REQ-PKG-03: the server can be installed and listed in the official MCP Registry."""

from __future__ import annotations

import json
import re
import subprocess
import sys
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


def _publish_workflow() -> str:
    return (ROOT / ".github" / "workflows" / "publish.yml").read_text(encoding="utf-8")


def test_publish_workflow_runs_on_version_tags_only() -> None:
    """REQ-PKG-04: publishing starts from a `v*` tag, never from a branch push."""
    workflow = _publish_workflow()
    assert 'tags: ["v*"]' in workflow
    assert "branches:" not in workflow


def test_publish_workflow_uses_oidc_and_no_secrets() -> None:
    """REQ-PKG-04: PyPI trusted publishing and the registry login use OIDC, not stored tokens."""
    workflow = _publish_workflow()
    assert "secrets." not in workflow
    assert "mcp-publisher login github-oidc" in workflow
    assert "pypa/gh-action-pypi-publish@" in workflow
    # id-token is granted per job, never for the whole workflow.
    assert workflow.count("id-token: write") == 2


def test_publish_workflow_checks_the_tag_against_the_versions() -> None:
    """REQ-PKG-04: a tag that differs from pyproject.toml or server.json stops the release."""
    assert "scripts/check_release_version.py" in _publish_workflow()
    guard = [sys.executable, str(ROOT / "scripts" / "check_release_version.py")]
    ok = subprocess.run([*guard, "v0.1.0"], capture_output=True, text=True, check=False)
    assert ok.returncode == 0, ok.stderr
    bad = subprocess.run([*guard, "v9.9.9"], capture_output=True, text=True, check=False)
    assert bad.returncode == 1
    assert "version mismatch" in bad.stderr


def test_publish_workflow_pins_every_action_to_a_commit() -> None:
    """REQ-PKG-04: third-party actions are pinned by full commit SHA."""
    uses = re.findall(r"uses:\s*(\S+)", _publish_workflow())
    assert uses
    for reference in uses:
        assert re.search(r"@[0-9a-f]{40}$", reference), reference
