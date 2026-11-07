"""Exercise theme configuration without requiring an Anki installation."""
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

root = Path(__file__).parent / 'glass_ui'
if not root.is_dir():
    root = Path(__file__).parent
config = json.loads((root / 'config.json').read_text())
actions = {}
aqt = ModuleType('aqt')
aqt.mw = SimpleNamespace(addonManager=SimpleNamespace(
    getConfig=lambda name: dict(config),
    setConfigAction=lambda name, action: actions.update({name: action}),
))
aqt.gui_hooks = SimpleNamespace(webview_will_set_content=[])
theme = ModuleType('aqt.theme')
theme.theme_manager = SimpleNamespace(night_mode=False)
sys.modules.update({'aqt': aqt, 'aqt.theme': theme})
spec = importlib.util.spec_from_file_location('glass_ui', root / '__init__.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert actions['glass_ui'] == module._show_settings
assert config == module._DEFAULTS

def render(name='DeckBrowser'):
    content = SimpleNamespace(head='existing')
    module._on_webview(content, type(name, (), {})())
    return content.head

assert '--gui-text: #f6f2ff' in render()
config['appearance'] = 'light'
assert '--gui-text: #272035' in render()
config['appearance'] = 'system'
assert '--gui-text: #272035' in render()
theme.theme_manager.night_mode = True
assert '--gui-text: #f6f2ff' in render()
assert render('Reviewer') == 'existing'
config['enabled'] = False
assert render() == 'existing'
config['enabled'] = True
config['font_size_px'] = 200
assert '--gui-font-size: 28px' in render()
print('PASS: defaults, config action, appearance modes, scope, disable, size limits')

scripts = {'main': [], 'top': [], 'bottom': []}
aqt.mw.web = SimpleNamespace(eval=scripts['main'].append)
aqt.mw.topWeb = SimpleNamespace(eval=scripts['top'].append)
aqt.mw.bottomWeb = SimpleNamespace(eval=scripts['bottom'].append)
aqt.mw.state = 'deckBrowser'
config['font_size_px'] = 23
module._apply_settings()
assert all(len(v) == 1 for v in scripts.values())
assert '--gui-font-size: 23.0px' in scripts['main'][-1]
assert 'el.remove()' in scripts['main'][-1]
config['enabled'] = False
module._apply_settings()
assert 'template.innerHTML = "";' in scripts['main'][-1]
aqt.mw.state = 'review'
module._apply_settings()
assert len(scripts['main']) == 2 and len(scripts['bottom']) == 2
assert len(scripts['top']) == 3
print('PASS: immediate apply, disable removes styles, reviewer is untouched')

config['enabled'] = True
assert 'body #study {' in render('Overview')
assert 'body #study {' not in render('DeckBrowser')
assert 'glass-ui-theme' in render('OverviewBottomBar')
aqt.mw.state = 'overview'
module._apply_settings()
assert 'body #study {' in scripts['main'][-1]
assert 'body #study {' not in scripts['top'][-1]
assert 'body #study {' not in scripts['bottom'][-1]
config['enabled'] = False
module._apply_settings()
assert 'template.innerHTML = "";' in scripts['main'][-1]
print('PASS: overview styling isolated, overview footer supported, live apply and disable')
