# Glass UI settings

Open **Tools → Add-ons → Glass UI → Config** for the settings window. Choose **Apply** to save and update immediately, or **Save** to apply and close. **Cancel** discards edits since the last Apply; **Restore defaults** resets the visible controls and takes effect after Apply or Save.

- `appearance`: `dark`, `light`, or `system` (match Anki). Light glass uses a pale panel and dark text; dark glass uses the configured panel and text colours.

- `enabled`: set `false` to stop styling.
- `panel_opacity`: value from `0.15` to `1.0`.
- `blur_px`: glass blur amount, `0` to `40`.
- `corner_radius_px`: rounding, `0` to `40`.
- `accent_color`, `text_color`, `panel_color`: hex colour values.
- `panel_max_width_px`: deck list maximum width, `400` to `1800`.
- `font_size_px`: deck text size, `12` to `28`; default `17`. The study summary and buttons scale with it.
- `row_padding_px`: vertical padding inside each deck row, `0` to `14`; default `4`.

For a roomier layout, use width `900`, font size `17`, and row padding `4`. For a compact layout, use width `735`, font size `13`, and row padding `3`. Larger text may require scrolling when many decks are expanded.

When upgrading, Anki may retain your previous configuration. Set `panel_max_width_px` to `900` if it is still `735`. Existing colour and transparency preferences are preserved.

This add-on **does not** modify, supply, or replace backgrounds or card templates.

Version 1.0 targets Qt 6 Anki desktop; a tested-version compatibility matrix has not yet been established. It focuses on deck-list sizing and common button typography, not native Qt dialogs or third-party widgets. Some layouts may require adjustments.

### Deck colours (v0.5)

Use the colour swatches in Config to open a colour picker:
- `highlight_color`: selected/hovered/focused row background; default `#cbb6f4`.
- `highlight_text_color`: highlighted deck name and expand/collapse control; default `#211638`.
- `text_color`: normal text in dark glass.
- `light_text_color`: normal text in light glass; default `#272035`.

Highlight colours apply in both appearance modes. Restore defaults resets these controls too. Click Apply or Save.

The Enable Glass UI checkbox must be checked for styling controls to affect the interface. Apply while unchecked removes the theme. Accent changes the deck-panel border and button hover borders. Appearance changes the glass panels, not the Windows settings-window appearance.

Overview and deck-list styles share the same controls. Interface text size also scales the overview title and Study Now button. For lower graphics cost, set Background blur to 0px. Apply updates the current deck list or overview without resetting study state.

Typography is fixed to Segoe UI with system fallbacks; there is no font picker. Interface text size remains adjustable.

Click the Accent colour swatch to choose any colour from the colour picker. Existing accent choices are retained. Click Apply or Save to use the chosen colour.

### Overview sizing

- `overview_width_px`: overview maximum width, 400–1400; default 760.
- `overview_padding_px`: space inside the overview panel, 8–48; default 16.
- `study_button_padding_px`: button vertical padding, 4–20; default 8. Horizontal padding is twice this value.

These settings are separate from deck-list sizing. Click Apply to see changes. The panel height follows its contents, including any calendar.
