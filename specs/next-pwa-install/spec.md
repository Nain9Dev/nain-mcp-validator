# Specification: Installable project page (Android and iOS)

Status: Implemented on `feat/pwa-install-mcp`, not merged

## Objective

A visitor on a phone can install `https://mcp.naindev.com/` from the browser and open it like an app: its own
icon and name on the home screen and a window with no browser bar. Android Chrome and iOS Safari are the
targets. The shared contract and the verified browser install criteria live in the portfolio repository
(`Nain9Dev/nain9dev.github.io`, `specs/next-pwa-install/spec.md`); this document applies them to this site.

Names approved by the owner on 2026-11-13: `short_name` `Nain MCP`, `name` `Nain MCP Validator`.

## Functional requirements (EARS)

- **INS-001**: The site shall publish `manifest.webmanifest` at the root of `site/`, and `site/index.html`
  shall link it with `<link rel="manifest" href="./manifest.webmanifest">`.
- **INS-002**: The manifest shall declare `id`, `start_url` and `scope` as `./`, `display` as `standalone`,
  `lang` as `en`, `dir` as `ltr`, `name` as `Nain MCP Validator`, `short_name` as `Nain MCP`, the page meta
  description as `description`, and `theme_color` and `background_color` as `#EDF1F6`. It shall not declare
  `prefer_related_applications`.
- **INS-003**: The manifest shall declare three PNG icons in `site/icons/` that exist at the declared size:
  192 px and 512 px with purpose `any`, and 512 px with purpose `maskable`.
- **INS-004**: The maskable icon and the 180 px `apple-touch-icon.png` shall be opaque edge to edge; the mark
  of the maskable icon shall sit inside the centred circle whose radius is 40% of the width.
- **INS-005**: The page shall carry the iOS tags: `apple-touch-icon`, `apple-mobile-web-app-title` equal to
  `Nain MCP`, `mobile-web-app-capable` and `apple-mobile-web-app-capable` set to `yes`, and
  `apple-mobile-web-app-status-bar-style` set to `default` (the page is light).
- **INS-006**: `pytest` shall fail if INS-001 to INS-005 regress (`tests/test_site_install.py`).

## Edge cases and error handling

- The page already uses relative paths (`./favicon.svg`), so the manifest does too. The page is one document
  at the host root.
- The site has no Content-Security-Policy; GitHub Pages serves the manifest and icons as plain files.
- `pages.yml` uploads the whole `site/` folder, so no workflow change is needed. Its `paths` filter already
  includes `site/**`.
- The page keeps its own `theme-color`; the manifest value paints the splash screen and the window before
  the first load.
- Offline: no service worker, so an installed window without network shows the browser's offline screen.

## Out of scope

- A service worker, offline page, cache or in-page install button (owner decision of 2026-11-13).
- Screenshots for the richer Android install dialog; a store package.

## Acceptance criteria

- `pytest -v`, `ruff check src tests` and `mypy src tests` pass.
- Chrome reports no installability error for the `site/` folder served at its root.
- After the deploy, `https://mcp.naindev.com/manifest.webmanifest` answers 200 and the owner installs the page
  on an Android phone and an iPhone: the icon shows the mark uncropped and the label reads `Nain MCP`.

## Session state

- Last updated: 2026-11-14, session pwa-install-mcp
- Done: T01 to T04.
- Verified: local pytest, ruff, mypy; `installabilityErrors` empty on `site/`.
- Next: T05 after the merge (live manifest, install on both phones).
- Blocked: nothing. T05 needs the owner's phones.
