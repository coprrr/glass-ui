"""Build the release archive with only distributable add-on files."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
source = root / 'glass_ui'
if not source.is_dir():
    source = root
output = root / 'Glass_UI_v1.0.ankiaddon'
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for name in ['__init__.py', 'settings.py', 'config.json', 'config.md',
                 'manifest.json', 'README.md', 'LICENSE']:
        archive.write(source / name, name)
    web = source / 'web' if (source / 'web').is_dir() else source
    for name in ['glass.css', 'overview.css']:
        archive.write(web / name, 'web/' + name)
with ZipFile(output) as archive:
    assert archive.testzip() is None
    assert {'__init__.py', 'settings.py', 'config.json', 'manifest.json',
            'web/glass.css', 'web/overview.css', 'LICENSE'} <= set(archive.namelist())
print(output)
