from demo_view import build as demo_view
"""Finish the synthetic walkthrough: trend, incomplete goal and closed pilot."""
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('task',ROOT/'ai-task/scripts/task.py')
task=importlib.util.module_from_spec(spec);spec.loader.exec_module(task)
room=ROOT/'examples/demo'
values=[
 ('source',dict(id='src_walkthrough',title='Synthetische Demo · Verlauf und Pilot',reference='demo-walkthrough.md',text='SYNTHETISCH. Abschnitt 1: Im gleichen Nutzertest am 2. Oktober waren die Einrichtungserfolgsquote 48%, die mediane Zeit bis zur ersten Aufgabe 18 Minuten und die Erstwochennutzung 33%. Abschnitt 2: Die Ideentest-Reichweite am 9. Oktober beträgt 10 von angestrebten 20 Teilnehmenden, Ausgang 0. Eine Zufriedenheitsmessung liegt noch nicht vor. Abschnitt 3: Der interne Pilot vom September wurde am 30. September anhand der vollständigen Abnahmecheckliste freigegeben; binärer Messwert 1.')),
 ('measurement',dict(id='msr_setup_early',title='Einrichtung · 2. Oktober',keyResultId='kr_setup',date='2026-10-02',value=48,sourceId='src_walkthrough',locator='Abschnitt 1, Einrichtung',confidence=.5)),
 ('measurement',dict(id='msr_time_early',title='Zeit · 2. Oktober',keyResultId='kr_time',date='2026-10-02',value=18,sourceId='src_walkthrough',locator='Abschnitt 1, Zeit',confidence=.4)),
 ('measurement',dict(id='msr_week_early',title='Nutzung · 2. Oktober',keyResultId='kr_week',date='2026-10-02',value=33,sourceId='src_walkthrough',locator='Abschnitt 1, Erstwochennutzung',confidence=.3)),
 ('task',dict(id='tsk_any',notes='Nächster Schritt aus dem OKR-Check-in: die Einrichtung auf wenige klare Schritte reduzieren. Beitrag zu kr_time. Ob es wirkt, wird im nächsten Nutzertest gemessen.',checklist=[dict(id='chk_steps',title='Aktuelle Schritte erfassen',completed=True),dict(id='chk_reduce',title='Überflüssige Schritte vereinfachen',completed=False),dict(id='chk_measure',title='Zeit im nächsten Test messen',completed=False)])),
 ('task',dict(id='tsk_recruit',title='Teilnehmende für den Ideentest gewinnen',status='active',scheduledDate='2026-10-12',listId='area_work',notes='Unterstützt das ambitionierte Lernziel. Rückmeldungen und Reichweite separat erfassen.')),
 ('objective',dict(id='obj_learning',title='Neue Ideen früh mit Nutzern prüfen',owner='Synthetisches Demoteam',startDate='2026-10-01',endDate='2026-12-31',goalType='aspirational',status='active')),
 ('key-result',dict(id='kr_reach',title='20 Teilnehmende für den Ideentest erreichen',objectiveId='obj_learning',direction='increase',baseline=0,target=20,unit='Teilnehmende',method='Eindeutige Teilnehmende im Testregister zählen',taskIds=['tsk_recruit'])),
 ('key-result',dict(id='kr_satisfaction',title='Zufriedenheit mit dem Einstieg erhöhen',objectiveId='obj_learning',direction='increase',baseline=3,target=4.5,unit='von 5 Punkten',method='Gleiche fünfstufige Frage nach dem Test',critical=True)),
 ('measurement',dict(id='msr_reach',title='Reichweite · 9. Oktober',keyResultId='kr_reach',date='2026-10-09',value=10,sourceId='src_walkthrough',locator='Abschnitt 2',confidence=.6)),
 ('review',dict(id='rev_learning',title='Lernziel · Check-in',objectiveId='obj_learning',date='2026-10-09',obstacles='Die Zufriedenheitsbefragung wurde noch nicht ausgewertet.',learnings='50% Teilmittel ist kein vollständiger Zielscore. Fehlende Messung bleibt unbekannt.',nextTaskIds=['tsk_recruit'])),
 ('project',dict(id='prj_pilot',title='Interner Pilot · abgeschlossen',areaId='area_work',status='completed',completedAt='2026-09-30',notes='Abgeschlossener vorheriger Zyklus: Freigabe mit belegter Checkliste.')),
 ('task',dict(id='tsk_pilot_accept',title='Interne Pilotabnahme dokumentieren',status='completed',completedAt='2026-09-30',isLogged=True,listId='prj_pilot',notes='Abnahme im synthetischen Beispiel vom 30. September dokumentiert.')),
 ('objective',dict(id='obj_pilot',title='September-Pilot verlässlich freigeben · abgeschlossen',owner='Synthetisches Demoteam',startDate='2026-09-01',endDate='2026-09-30',goalType='committed',status='closed')),
 ('key-result',dict(id='kr_pilot_accept',title='Pilot anhand der Abnahmecheckliste freigegeben',objectiveId='obj_pilot',direction='binary',baseline=0,target=1,unit='Abnahme',method='Freigabe nur bei bestätigter vollständiger Abnahmecheckliste',critical=True,taskIds=['tsk_pilot_accept'],projectIds=['prj_pilot'])),
 ('measurement',dict(id='msr_pilot_accept',title='Pilotabnahme · 30. September',keyResultId='kr_pilot_accept',date='2026-09-30',value=1,sourceId='src_walkthrough',locator='Abschnitt 3',confidence=1)),
 ('review',dict(id='rev_pilot_close',title='September-Pilot · Abschlussreview',objectiveId='obj_pilot',date='2026-09-30',reviewType='closeout',outcome='achieved',obstacles='Keine offenen Abnahmepunkte im Beispiel.',learnings='Der Pilot ist freigegeben. Das beweist noch keine verbesserte Einrichtung im Oktober; dafür messen wir eigene Ergebnisse.')),
 ('knowledge',dict(id='knw_okr_context',title='Wie Aufgaben und OKR in der Demo zusammenhängen',notes='Beginne im Bereich Ziele & Wirkung. Das Einstiegsziel zeigt vollständige Messungen; das Lernziel zeigt eine Messlücke; der September-Pilot zeigt einen Abschlussreview.',recordIds=['obj_entry','obj_learning','obj_pilot','tsk_any'],claims=[dict(text='Im Beispiel liegt für das Lernziel noch keine Zufriedenheitsmessung vor.',sourceId='src_walkthrough',locator='Abschnitt 2'),dict(text='Der September-Pilot wurde am 30. September anhand der vollständigen Checkliste freigegeben.',sourceId='src_walkthrough',locator='Abschnitt 3')]))
]
state,_=task.load(room)
if 'src_walkthrough' not in state['records']['source']:
 p=task.plan(room,[{'op':'upsert','kind':k,'record':r} for k,r in values],'process:demo','SYNTHETIC_WALKTHROUGH','2026-10-09')
 task.apply(room,p,p['sha256'])
state,generation=task.load(room)
(ROOT/'docs/demo.html').write_bytes(demo_view(task, state))
report={x['objective']['id']:x for x in task.okr.report(state,'2026-10-09')}
assert abs(report['obj_entry']['progress']-7/15)<1e-10
assert report['obj_learning']['progress'] is None and report['obj_learning']['partialMean']==.5
assert report['obj_pilot']['progress']==1 and report['obj_pilot']['reviews'][0]['outcome']=='achieved'
assert len(report['obj_entry']['keyResults'])==3
print('Complete synthetic walkthrough verified:',generation)
