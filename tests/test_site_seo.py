"""Search and AI-engine discoverability baseline for the public project page (REQ-SEO-01)."""

import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "site"
HOST_ROOT = "https://mcp.naindev.com/"
AUTHOR_ID = "https://www.naindev.com/#person"


def _html() -> str:
    return (SITE / "index.html").read_text(encoding="utf-8")


def _meta(html: str, key: str, value: str) -> list[str]:
    pattern = rf'<meta\s+{key}="{re.escape(value)}"\s+content="([^"]*)"'
    return re.findall(pattern, html)


def test_single_canonical_equals_host_root() -> None:
    hrefs = re.findall(r'<link\s+rel="canonical"\s+href="([^"]*)"', _html())
    assert hrefs == [HOST_ROOT]


def test_single_description_has_sensible_length() -> None:
    descriptions = _meta(_html(), "name", "description")
    assert len(descriptions) == 1
    assert 70 <= len(descriptions[0]) <= 160


def test_open_graph_and_twitter_cards() -> None:
    html = _html()
    assert _meta(html, "property", "og:type") == ["website"]
    assert _meta(html, "property", "og:url") == [HOST_ROOT]
    assert _meta(html, "property", "og:site_name") == ["nain-mcp-validator"]
    assert len(_meta(html, "property", "og:title")) == 1
    assert _meta(html, "property", "og:description") == _meta(html, "name", "description")
    images = _meta(html, "property", "og:image")
    assert len(images) == 1 and images[0].startswith("https://")
    assert _meta(html, "name", "twitter:card") == ["summary_large_image"]
    assert _meta(html, "name", "twitter:image") == images


def test_author_link_and_single_h1() -> None:
    html = _html()
    assert '<link rel="author" href="https://www.naindev.com/">' in html
    assert len(re.findall(r"<h1[\s>]", html)) == 1


def test_json_ld_software_application() -> None:
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', _html(), flags=re.S
    )
    assert len(blocks) == 1
    assert "<" not in blocks[0]
    data = json.loads(blocks[0])
    assert data["@type"] == "SoftwareApplication"
    assert data["url"] == HOST_ROOT
    assert data["author"]["@id"] == AUTHOR_ID
    assert data["isAccessibleForFree"] is True
    assert data["operatingSystem"] == "Web"


def test_robots_advertises_sitemap() -> None:
    robots = (SITE / "robots.txt").read_text(encoding="utf-8").splitlines()
    assert "User-agent: *" in robots
    assert "Allow: /" in robots
    assert f"Sitemap: {HOST_ROOT}sitemap.xml" in robots
    assert not any(line.startswith("Disallow: /") for line in robots)


def test_sitemap_lists_canonical_root() -> None:
    sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
    assert re.findall(r"<loc>([^<]*)</loc>", sitemap) == [HOST_ROOT]


def test_llms_txt_starts_with_h1() -> None:
    text = (SITE / "llms.txt").read_text(encoding="utf-8")
    assert text.startswith("# ")
    assert "\n> " in text
