"""Build a byte-reproducible standalone Agent Skills ZIP."""
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build():
    folder = ROOT / 'ai-task'
    files = sorted(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    output = ROOT / 'dist/ai-task.skill'
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2026, 10, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    checksum = hashlib.sha256(output.read_bytes()).hexdigest()
    (ROOT / 'dist/ai-task.skill.sha256').write_text(checksum + '  ai-task.skill\n')
    if (ROOT / "docs/demo.html").exists():
        (ROOT / "docs/ai-task.skill").write_bytes(output.read_bytes())
        (ROOT / "docs/ai-task.skill.sha256").write_bytes((ROOT / "dist/ai-task.skill.sha256").read_bytes())
    return checksum


if __name__ == '__main__':
    print(build())
