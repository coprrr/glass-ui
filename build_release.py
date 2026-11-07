"""Build the release archive with only distributable add-on files."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parent
source = root / 'glass_ui'
output = root / 'Glass_UI_v1.0.ankiaddon'
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(source.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            archive.write(path, path.relative_to(source).as_posix())
with ZipFile(output) as archive:
    assert archive.testzip() is None
    assert {'__init__.py', 'settings.py', 'config.json', 'manifest.json',
            'web/glass.css', 'web/overview.css', 'LICENSE'} <= set(archive.namelist())
print(output)
