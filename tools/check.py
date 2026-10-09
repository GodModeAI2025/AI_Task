from demo_view import build as demo_view
"""Offline regression, skill references, demo integrity and package checks."""
import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'work').mkdir(exist_ok=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-v'], check=True, cwd=ROOT)
skill = ROOT / 'ai-task/SKILL.md'
content = skill.read_text()
assert content.startswith('---\nname: ai-task\ndescription:'), 'Missing skill frontmatter'
for path in re.findall(r'\]\((references/[^)]+)\)', content):
    assert (skill.parent / path).is_file(), path
spec = importlib.util.spec_from_file_location('runtime', ROOT / 'ai-task/scripts/task.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)
if (ROOT / 'examples/demo/meta/CURRENT').exists():
    runtime.load(ROOT / 'examples/demo')
    for generation in (ROOT / 'examples/demo/meta/generations').iterdir():
        runtime.verify_generation(ROOT / 'examples/demo', generation.name)
    assert (ROOT / 'docs/demo.html').read_bytes() == demo_view(runtime, runtime.load(ROOT / 'examples/demo')[0])
subprocess.run([sys.executable, str(ROOT / 'tools/package.py')], check=True)
first = (ROOT / 'dist/ai-task.skill').read_bytes()
subprocess.run([sys.executable, str(ROOT / 'tools/package.py')], check=True)
assert first == (ROOT / 'dist/ai-task.skill').read_bytes(), 'Package is not reproducible'
with zipfile.ZipFile(ROOT / 'dist/ai-task.skill') as archive:
    assert 'ai-task/SKILL.md' in archive.namelist()
    assert not any('..' in name.split('/') or name.startswith('/') for name in archive.namelist())
    assert archive.testzip() is None
print('All checks passed; package SHA-256:', hashlib.sha256(first).hexdigest())
