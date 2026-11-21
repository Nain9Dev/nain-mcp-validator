"""Stop a release when the tag, pyproject.toml and server.json disagree on the version.

Reads the tag from GITHUB_REF_NAME (for example `v0.1.0`) unless a tag is passed as the first
argument. Exits with 1 and prints the mismatching values.
"""

from __future__ import annotations

import json
import os
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def versions(tag: str) -> dict[str, str]:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    server = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    return {
        "tag": tag.removeprefix("v"),
        "pyproject.toml": project,
        "server.json": server["version"],
        "server.json package": server["packages"][0]["version"],
    }


def main(argv: list[str]) -> int:
    tag = argv[1] if len(argv) > 1 else os.environ.get("GITHUB_REF_NAME", "")
    found = versions(tag)
    if len(set(found.values())) != 1:
        print(f"version mismatch: {found}", file=sys.stderr)
        return 1
    print(f"release version {found['tag']} is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
