# Glass UI for Anki

Version 1.0 — a configurable glass-style interface for Anki desktop.

## Features

- Coordinated deck-list and deck-overview panels.
- Dark glass, light glass, or match Anki appearance.
- Adjustable opacity, blur, rounding, and full colour pickers for accent, text and highlights.
- Segoe UI typography with system fallbacks, adjustable text size and spacing.
- Settings window with Apply, Save, Cancel, and Restore defaults.
- Styling updates immediately when you click Apply.

## Install

Download `Glass_UI_v1.0.ankiaddon`. In Anki choose **Tools → Add-ons → Install from file**, select the file, and restart Anki. Open **Tools → Add-ons → Glass UI → Config** to customize it.

Check **Enable Glass UI** to use the theme. **Apply** saves and updates the current screen. **Save** applies and closes. **Cancel** discards changes since the last Apply. Restore defaults resets the visible controls; click Apply or Save to keep them.

When switching from a manually installed copy to AnkiWeb, disable the manual copy first to avoid running two copies.

## Performance

No background polling, DOM observers or animated blur. Apply replaces the add-on's style blocks without rebuilding the study page. For lower graphics cost, set blur to **0px**. Performance depends on your hardware, wallpaper and other add-ons.

## Troubleshooting

After installing an update, restart Anki once. If settings appear ineffective, check Enable Glass UI and click Apply. If a conflict occurs, disable Glass UI and report the Anki version, operating system, affected screen and other appearance add-ons in a GitHub issue.

## Development

This repository intentionally keeps all source files in one folder, including glass.css and overview.css. Run `python -B check_glass.py` for checks and `python build_release.py` to create the installable archive. The build script packages the required files and places stylesheets in web/ automatically.

## License

GNU Affero General Public License, version 3 or later (AGPL-3.0-or-later). See LICENSE. This preserves the license declared in the original Glass UI package.

### Compact deck overview

Config includes independent Overview panel width, Overview panel padding and Study Now button padding controls. Defaults are 760px, 16px and 8px. They do not shrink the deck list. Calendar contents keep their own layout; a narrow panel scrolls horizontally if needed. The panel height follows its contents.
