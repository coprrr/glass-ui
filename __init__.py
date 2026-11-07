"""Glass UI for Anki. Interface styling only; no wallpaper manipulation."""
from __future__ import annotations

from pathlib import Path
import json
from types import SimpleNamespace

from aqt import gui_hooks, mw

_ROOT = Path(__file__).resolve().parent
_WEB = _ROOT / 'web' if (_ROOT / 'web').is_dir() else _ROOT
_CSS = (_WEB / 'glass.css').read_text(encoding='utf-8')
_OVERVIEW_CSS = (_WEB / 'overview.css').read_text(encoding='utf-8')
_DEFAULTS = {
    'appearance': 'dark',
    'enabled': True,
    'panel_opacity': 0.61,
    'blur_px': 12,
    'corner_radius_px': 17,
    'accent_color': '#b99aff',
    'text_color': '#f6f2ff',
    'light_text_color': '#272035',
    'highlight_color': '#cbb6f4',
    'highlight_text_color': '#211638',
    'panel_color': '#211638',
    'panel_max_width_px': 900,
    'font_size_px': 17,
    'row_padding_px': 4,
    'overview_width_px': 760,
    'overview_padding_px': 16,
    'study_button_padding_px': 8,
}


def _config():
    data = mw.addonManager.getConfig(__name__) or {}
    return {**_DEFAULTS, **data}


def _clamp(value, low, high, default):
    try:
        return max(low, min(high, float(value)))
    except (ValueError, TypeError):
        return default


def _hex(value, fallback):
    value = str(value).strip()
    if len(value) in (4, 7) and value.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in value[1:]):
        return value
    return fallback


def _on_webview(wc, context):
    # Limit modifications to Anki's main deck/overview/toolbar webviews.
    if context is None:
        return
    klass = type(context).__name__
    if klass not in {'DeckBrowser', 'Overview', 'Toolbar', 'BottomBar', 'DeckBrowserBottomBar', 'OverviewBottomBar'}:
        return

    cfg = _config()
    if not cfg.get('enabled', True):
        return

    from aqt.theme import theme_manager
    appearance = cfg.get('appearance', 'dark')
    light = appearance == 'light' or (appearance == 'system' and not theme_manager.night_mode)

    font = '"Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, Arial, sans-serif'
    alpha = _clamp(cfg['panel_opacity'], 0.15, 1.0, .76)
    blur = _clamp(cfg['blur_px'], 0, 40, 14)
    radius = _clamp(cfg['corner_radius_px'], 0, 40, 18)
    width = _clamp(cfg['panel_max_width_px'], 400, 1800, 900)
    font_size = _clamp(cfg['font_size_px'], 12, 28, 17)
    row_padding = _clamp(cfg['row_padding_px'], 0, 14, 4)
    overview_width = _clamp(cfg['overview_width_px'], 400, 1400, 760)
    overview_padding = _clamp(cfg['overview_padding_px'], 8, 48, 16)
    study_padding = _clamp(cfg['study_button_padding_px'], 4, 20, 8)
    accent = _hex(cfg['accent_color'], '#b99aff')
    fg = _hex(cfg['text_color'], '#f6f2ff')
    panel = _hex(cfg['panel_color'], '#211638')
    if light:
        fg, panel = _hex(cfg['light_text_color'], '#272035'), '#f4efff'
    highlight = _hex(cfg['highlight_color'], '#cbb6f4')
    highlight_text = _hex(cfg['highlight_text_color'], '#211638')
    # CSS custom properties preserve a single configuration for every component.
    color6 = panel.lstrip('#')
    if len(color6) == 3:
        color6 = ''.join(c * 2 for c in color6)
    rgb = tuple(int(color6[i:i+2], 16) for i in (0, 2, 4))
    panel_bg = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'
    vars_css = f'''<style id="glass-ui-settings">
:root {{
  --gui-font: {font};
  --gui-alpha: {alpha};
  --gui-blur: {blur}px;
  --gui-radius: {radius}px;
  --gui-max-width: {width}px;
  --gui-font-size: {font_size}px;
  --gui-row-padding: {row_padding}px;
  --gui-overview-width: {overview_width}px;
  --gui-overview-padding: {overview_padding}px;
  --gui-study-padding: {study_padding}px;
  --gui-accent: {accent};
  --gui-text: {fg};
  --gui-highlight: {highlight};
  --gui-highlight-text: {highlight_text};
  --gui-panel: {panel};
  --gui-panel-bg: {panel_bg};
}}
</style>'''
    # Append-only: does not replace other add-ons' style content or backgrounds.
    css = _CSS + (_OVERVIEW_CSS if klass == 'Overview' else '')
    wc.head += vars_css + '<style id="glass-ui-theme">' + css + '</style>'


gui_hooks.webview_will_set_content.append(_on_webview)


def _show_settings():
    from .settings import GlassSettings
    GlassSettings(mw, __name__, _config(), _DEFAULTS, _apply_settings).exec()


def _apply_settings():
    """Replace only our styles on loaded main-window pages, including disable."""
    views = []
    state = getattr(mw, 'state', None)
    if state in {'deckBrowser', 'overview'}:
        views.append((getattr(mw, 'web', None), 'Overview' if state == 'overview' else 'DeckBrowser'))
        views.append((getattr(mw, 'bottomWeb', None), 'BottomBar'))
    views.append((getattr(mw, 'topWeb', None), 'Toolbar'))
    for view, context_name in views:
        if view is None:
            continue
        content = SimpleNamespace(head='')
        _on_webview(content, type(context_name, (), {})())
        script = '''(() => {
      document.querySelectorAll('#glass-ui-settings, #glass-ui-theme').forEach(el => el.remove());
      const template = document.createElement('template');
      template.innerHTML = %s;
      document.head.appendChild(template.content);
    })();''' % json.dumps(content.head)
        view.eval(script)


mw.addonManager.setConfigAction(__name__, _show_settings)
