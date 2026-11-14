"""Install contract of the project page: manifest, icons and head tags (REQ-PWA-01)."""

import json
import re
import struct
import zlib
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / "site"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_ICONS = [
    ("./icons/icon-192.png", "192x192", "any"),
    ("./icons/icon-512.png", "512x512", "any"),
    ("./icons/icon-maskable-512.png", "512x512", "maskable"),
]


def _html() -> str:
    return (SITE / "index.html").read_text(encoding="utf-8")


def _manifest() -> dict[str, object]:
    manifest: dict[str, object] = json.loads(
        (SITE / "manifest.webmanifest").read_text(encoding="utf-8")
    )
    return manifest


def _meta(html: str, name: str) -> list[str]:
    return re.findall(rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"', html)


def _png_size(path: Path) -> tuple[int, int, int]:
    """Return (width, height, colour type) read from the IHDR chunk of a PNG file."""
    header = path.read_bytes()[:26]
    assert header[:8] == PNG_SIGNATURE, f"{path.name} is not a PNG file"
    width, height = struct.unpack(">II", header[16:24])
    return width, height, header[25]


def _is_opaque(path: Path) -> bool:
    """Decode an 8-bit RGB or RGBA PNG and report whether every pixel is fully opaque."""
    data = path.read_bytes()
    _, _, colour_type = _png_size(path)
    if colour_type == 2:
        return True
    assert colour_type == 6 and data[24] == 8, f"{path.name}: expected 8-bit RGB or RGBA"
    width = struct.unpack(">I", data[16:20])[0]
    idat, at = b"", 8
    while at < len(data):
        length, kind = struct.unpack(">I4s", data[at : at + 8])
        if kind == b"IDAT":
            idat += data[at + 8 : at + 8 + length]
        at += 12 + length
    raw, stride, previous = zlib.decompress(idat), width * 4, bytearray(width * 4)
    for start in range(0, len(raw), stride + 1):
        filter_type, line = raw[start], bytearray(raw[start + 1 : start + 1 + stride])
        for i in range(stride):
            left = line[i - 4] if i >= 4 else 0
            up, up_left = previous[i], (previous[i - 4] if i >= 4 else 0)
            if filter_type == 1:
                line[i] = (line[i] + left) & 255
            elif filter_type == 2:
                line[i] = (line[i] + up) & 255
            elif filter_type == 3:
                line[i] = (line[i] + (left + up) // 2) & 255
            elif filter_type == 4:
                p = left + up - up_left
                best = min((abs(p - left), left), (abs(p - up), up), (abs(p - up_left), up_left))
                line[i] = (line[i] + best[1]) & 255
        if any(a != 255 for a in line[3::4]):
            return False
        previous = line
    return True


def test_manifest_names_the_app_and_opens_it_standalone() -> None:
    manifest = _manifest()
    assert manifest["name"] == "Nain MCP Validator"
    assert manifest["short_name"] == "Nain MCP"
    assert manifest["description"] == _meta(_html(), "description")[0]
    assert manifest["lang"] == "en"
    assert manifest["dir"] == "ltr"
    assert manifest["id"] == manifest["start_url"] == manifest["scope"] == "./"
    assert manifest["display"] == "standalone"
    assert manifest["theme_color"] == manifest["background_color"] == "#EDF1F6"
    assert _meta(_html(), "theme-color") == ["#EDF1F6"]
    assert "prefer_related_applications" not in manifest


def test_manifest_icons_exist_at_their_declared_size() -> None:
    manifest = _manifest()
    icons = manifest["icons"]
    assert isinstance(icons, list)
    assert [(i["src"], i["sizes"], i["purpose"]) for i in icons] == EXPECTED_ICONS
    for icon in icons:
        assert icon["type"] == "image/png"
        width, height, _ = _png_size(SITE / icon["src"])
        assert f"{width}x{height}" == icon["sizes"], icon["src"]


def test_maskable_and_apple_icons_are_opaque() -> None:
    # A transparent pixel would be filled by the launcher with its own colour.
    assert _is_opaque(SITE / "icons" / "icon-maskable-512.png")
    assert _png_size(SITE / "icons" / "apple-touch-icon.png")[:2] == (180, 180)
    assert _is_opaque(SITE / "icons" / "apple-touch-icon.png")


def test_page_links_manifest_and_carries_ios_tags() -> None:
    html = _html()
    assert re.findall(r'<link\s+rel="manifest"\s+href="([^"]*)"', html) == [
        "./manifest.webmanifest"
    ]
    assert re.findall(r'<link\s+rel="apple-touch-icon"\s+href="([^"]*)"', html) == [
        "./icons/apple-touch-icon.png"
    ]
    assert _meta(html, "mobile-web-app-capable") == ["yes"]
    assert _meta(html, "apple-mobile-web-app-capable") == ["yes"]
    assert _meta(html, "apple-mobile-web-app-title") == ["Nain MCP"]
    assert _meta(html, "apple-mobile-web-app-status-bar-style") == ["default"]
