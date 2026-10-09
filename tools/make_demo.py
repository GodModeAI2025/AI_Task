from demo_view import build as demo_view
"""Build a synthetic example only; never seed a personal workspace."""
import importlib.util
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('task', ROOT / 'ai-task/scripts/task.py')
task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task)


def build():
    target = ROOT / 'examples/demo'
    if target.exists():
        raise ValueError('Demo already exists; preserve it instead of overwriting')
    (ROOT / 'work').mkdir(exist_ok=True)
    temp = Path(tempfile.mkdtemp(dir=ROOT / 'work'))
    try:
        room = temp / 'demo'
        p = task.init_plan(dict(purpose='Ein klarer Kopf für den Launch.', audience='Synthetisches Demoteam', language='de',
                                timezone='Europe/Berlin', tone='Klar, freundlich, du', boundaries='Nur synthetische Beispieldaten'), today='2026-10-09')
        task.apply(room, p, p['sha256'])
        values = [
            ('area', dict(id='area_work', title='Arbeit')),
            ('area', dict(id='area_personal', title='Persönlich')),
            ('project', dict(id='prj_launch', title='Launch vorbereiten', areaId='area_work', notes='Ein überprüfbares Beispielprojekt.')),
            ('heading', dict(id='hdg_launch', title='Vor dem Start', projectId='prj_launch')),
            ('tag', dict(id='tag_focus', title='Fokus')),
            ('task', dict(id='tsk_inbox', title='Idee für den nächsten Teamtermin festhalten', notes='Erst sammeln, später einordnen.')),
            ('task', dict(id='tsk_brief', title='Launch-Briefing abstimmen', status='active', scheduledDate='2026-10-09', deadline='2026-10-12', listId='prj_launch', headingId='hdg_launch', tags=['tag_focus'], notes='Die Entscheidung und den Kontext findest du im Wissensbereich.', checklist=[dict(id='chk_read', title='Entwurf lesen', completed=True), dict(id='chk_confirm', title='Offene Punkte klären', completed=False)])),
            ('task', dict(id='tsk_vendor', title='Rückmeldung vom Lieferanten prüfen', status='active', deadline='2026-10-08', listId='prj_launch', notes='Überfällige Deadline: heute sichtbar, auch ohne Plantermin.')),
            ('task', dict(id='tsk_evening', title='Den Tag in Ruhe abschließen', status='active', scheduledDate='2026-10-09', isEvening=True, listId='area_personal')),
            ('task', dict(id='tsk_next', title='Teamdemo zeigen', status='active', scheduledDate='2026-10-12', listId='prj_launch')),
            ('task', dict(id='tsk_any', title='Checkliste für die Übergabe schreiben', status='active', listId='prj_launch')),
            ('task', dict(id='tsk_later', title='Ideen für Version zwei sammeln', status='active', isSomeday=True, listId='prj_launch')),
            ('task', dict(id='tsk_done', title='Zielbild festhalten', status='completed', completedAt='2026-10-08', isLogged=True, listId='prj_launch')),
            ('task', dict(id='tsk_trash', title='Überholte Demoidee', status='trashed', trashedAt='2026-10-08', previousStatus=None)),
            ('task', dict(id='tsk_repeat', title='Wöchentlicher Projektcheck', status='active', isTemplate=True, rrule='FREQ=WEEKLY;BYDAY=MO', nextOccurrence='2026-10-12', listId='prj_launch', checklist=[dict(id='chk_deadlines', title='Deadlines prüfen', completed=False)])),
            ('source', dict(id='src_demo', title='Synthetisches Launch-Protokoll', reference='demo-launch-notes.md', text='SYNTHETISCHES BEISPIEL. Abschnitt 1: Das Launch-Briefing wird vor der Teamdemo abgestimmt. Die Teamdemo ist für den 12. Oktober 2026 geplant.')),
            ('knowledge', dict(id='knw_launch', title='Warum das Briefing zuerst kommt', notes='Beispielwissen mit einem konkreten Beleg.', recordIds=['tsk_brief', 'prj_launch'], claims=[dict(text='Im Beispiel wird das Launch-Briefing vor der Teamdemo abgestimmt.', sourceId='src_demo', locator='Abschnitt 1, Satz 1')]))
        ]
        p = task.plan(room, [{'op': 'upsert', 'kind': k, 'record': r} for k, r in values], 'process:demo', 'SYNTHETIC', '2026-10-09')
        task.apply(room, p, p['sha256'])
        target.parent.mkdir(exist_ok=True)
        shutil.copytree(room, target)
        state, generation = task.load(target)
        (ROOT / 'docs/demo.html').write_bytes(demo_view(task, state))
        print('Synthetic demo generation:', generation)
    finally:
        shutil.rmtree(temp)


if __name__ == '__main__':
    build()
