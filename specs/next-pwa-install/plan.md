# Plan: Installable project page

## Published folder

`.github/workflows/pages.yml` uploads `path: site` with no build step and no copy list, so every file under
`site/` is published as a file at the host root. Pages has no SPA fallback and the page sets no
Content-Security-Policy. No workflow change.

## Files

| File | Change |
| :--- | :--- |
| `site/manifest.webmanifest` | New. Values in INS-002; paths relative (`./`) like the rest of the page |
| `site/icons/icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png` | New, generated from `site/favicon.svg` |
| `site/index.html` | Manifest link, `apple-touch-icon` and four meta tags after the existing `rel="icon"` link |
| `tests/test_site_install.py` | New. Reads the manifest, the PNG headers and pixels, and the head tags with the standard library only |
| `docs/01-requirements.md` | New row `REQ-PWA-01` |

## Icons

The favicon is the mark on a `#0047AB` rounded tile, so the tile colour is the background of the maskable and
Apple icons. Regenerate with:

```
node make-install-icons.mjs --source site/favicon.svg --out site/icons --bg "#0047AB" --maskable-scale 0.85 --apple-scale 1
```

The script renders with `sharp` from the portfolio worktree; this repository gains no dependency. At 85% of
the width the tile of the favicon blends into the background and its three strokes cover 13% of the maskable
icon, inside the safe zone.

## Decisions

- `theme_color` and `background_color` reuse the page `theme-color` (`#EDF1F6`): the page is light and paints
  that colour first.
- The iOS status bar style is `default` because the page is light.
- The test checks opacity by decoding the PNG with `zlib`, so it needs no image library.

## Test

`pytest -v` in `.github/workflows/ci.yml` collects `tests/`, so the new file runs in CI. It failed with four
failures before the files above existed and passes after.
