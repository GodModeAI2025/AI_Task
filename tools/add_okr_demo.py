from demo_view import build as demo_view
"""Extend only the tracked synthetic demo through a normal verified transaction."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('task', ROOT / 'ai-task/scripts/task.py')
task = importlib.util.module_from_spec(spec);spec.loader.exec_module(task)
room = ROOT / 'examples/demo'
values = [
 ('source', dict(id='src_okr', title='Synthetischer Nutzertest · Oktober', reference='demo-okr-test.md', text='SYNTHETISCHE MESSWERTE. Tabelle 1: Erfolgreiche Einrichtung: Ausgang 40%, Ziel 80%, Ist 60%. Tabelle 2: Median bis zur ersten Aufgabe: Ausgang 20 Minuten, Ziel 8 Minuten, Ist 14 Minuten. Tabelle 3: Nutzer mit erledigter Aufgabe in Woche eins: Ausgang 30%, Ziel 60%, Ist 42%. Gleiches Testprotokoll im Beispiel.')),
 ('objective', dict(id='obj_entry', title='Neue Nutzer finden schnell einen verlässlichen Einstieg', owner='Synthetisches Demoteam', startDate='2026-10-01', endDate='2026-12-31', goalType='committed', status='active')),
 ('key-result', dict(id='kr_setup', title='Erfolgreiche Einrichtung verbessern', objectiveId='obj_entry', direction='increase', baseline=40, target=80, unit='%', method='Anteil erfolgreicher Einrichtung im gleichen Nutzertest', critical=True, taskIds=['tsk_brief'], projectIds=['prj_launch'])),
 ('key-result', dict(id='kr_time', title='Zeit bis zur ersten Aufgabe reduzieren', objectiveId='obj_entry', direction='decrease', baseline=20, target=8, unit='Minuten', method='Median der gemessenen Zeit bis zur ersten Aufgabe', taskIds=['tsk_any'], projectIds=['prj_launch'])),
 ('key-result', dict(id='kr_week', title='Aktive Nutzung in der ersten Woche erhöhen', objectiveId='obj_entry', direction='increase', baseline=30, target=60, unit='%', method='Anteil neuer Nutzer mit einer erledigten Aufgabe binnen sieben Tagen', taskIds=['tsk_next'])),
 ('measurement', dict(id='msr_setup', title='Einrichtung · 9. Oktober', keyResultId='kr_setup', date='2026-10-09', value=60, sourceId='src_okr', locator='Tabelle 1', confidence=.7)),
 ('measurement', dict(id='msr_time', title='Zeit · 9. Oktober', keyResultId='kr_time', date='2026-10-09', value=14, sourceId='src_okr', locator='Tabelle 2', confidence=.6)),
 ('measurement', dict(id='msr_week', title='Nutzung · 9. Oktober', keyResultId='kr_week', date='2026-10-09', value=42, sourceId='src_okr', locator='Tabelle 3', confidence=.5)),
 ('review', dict(id='rev_week', title='Wöchentlicher Check-in', objectiveId='obj_entry', date='2026-10-09', obstacles='Die Einrichtung ist im Beispiel noch zu aufwendig.', learnings='Einrichtung und Erstnutzung getrennt messen; erledigte Aufgaben beweisen keine verbesserte Erfolgsquote.', nextTaskIds=['tsk_any','tsk_brief']))
]
state, _ = task.load(room)
if not state['records'].get('objective', {}).get('obj_entry'):
 p = task.plan(room, [{'op':'upsert','kind':k,'record':r} for k,r in values], 'process:demo', 'SYNTHETIC_OKR', '2026-10-09')
 task.apply(room,p,p['sha256'])
state, generation = task.load(room)
(ROOT / 'docs/demo.html').write_bytes(demo_view(task, state))
print('OKR demo verified:', generation)
print('Measured progress:', task.okr.report(state,'2026-10-09')[0]['progress'])
