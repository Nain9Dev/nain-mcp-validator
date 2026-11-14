# Tasks: Installable project page

Labels: `[A]` agent alone, `[M]` mixed, `[H]` owner only.

- [x] **T01 [A]** Write `tests/test_site_install.py` and see it fail. Done when four tests fail on the
  unchanged site (INS-001 to INS-006).
- [x] **T02 [A]** Generate the four icons from `site/favicon.svg` with the command in `plan.md`. Done when the
  PNG files show the mark centred and uncropped.
- [x] **T03 [A]** Add `site/manifest.webmanifest` and the head tags in `site/index.html`. Done when the new
  tests pass.
- [x] **T04 [A]** Add `REQ-PWA-01` to `docs/01-requirements.md`. Done when the row names its test.
- [ ] **T05 [H]** After the merge, check that `https://mcp.naindev.com/manifest.webmanifest` answers 200 and
  install the page on an Android phone and an iPhone. Done when the icon, the `Nain MCP` label and the
  window without a browser bar are confirmed on both.
