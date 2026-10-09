import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('okr_runtime', ROOT / 'ai-task/scripts/task.py')
task = importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(task)


class OKRTests(unittest.TestCase):
 def setUp(self):
  (ROOT / 'work').mkdir(exist_ok=True)
  self.temp = Path(tempfile.mkdtemp(dir=ROOT / 'work'));self.room = self.temp / 'room'
  self.identity = dict(purpose='Synthetic OKR', audience='Demo', language='de', timezone='Europe/Berlin', tone='clear', boundaries='Synthetic only')
  p = task.init_plan(self.identity, today='2026-10-01');task.apply(self.room, p, p['sha256'])
  self.change([('source', dict(id='src_test', title='Test', reference='test.md', text='Synthetic measurements, table 1')),
               ('objective', dict(id='obj_test', title='Reliable entry', owner='Demo', startDate='2026-10-01', endDate='2026-12-31', status='active')),
               ('task', dict(id='tsk_work', title='Improve onboarding', status='active')),
               ('key-result', dict(id='kr_up', title='Success', objectiveId='obj_test', direction='increase', baseline=40, target=80, unit='%', method='Fixed user test', critical=True, taskIds=['tsk_work'])),
               ('key-result', dict(id='kr_down', title='Time', objectiveId='obj_test', direction='decrease', baseline=20, target=8, unit='minutes', method='Median elapsed time')),
               ('key-result', dict(id='kr_binary', title='Approval', objectiveId='obj_test', direction='binary', baseline=0, target=1, unit='acceptance', method='Signed acceptance'))])
 def tearDown(self):shutil.rmtree(self.temp)
 def change(self, values, today='2026-10-01'):
  actions = [{'op':'upsert','kind':k,'record':r} for k,r in values]
  p = task.plan(self.room, actions, 'agent/test', 'TEST', today);task.apply(self.room,p,p['sha256'])
 def measure(self, ident, kr, value, day='2026-10-09', **extra):
  self.change([('measurement', dict(id=ident,title='Measurement',keyResultId=kr,date=day,value=value,sourceId='src_test',locator='table 1',**extra))], today=day)
 def report(self,today='2026-10-09'):return task.okr.report(task.load(self.room)[0],today)[0]
 def test_unknown_and_partial_average(self):
  self.assertIsNone(self.report()['progress'])
  self.measure('msr_up','kr_up',60)
  r=self.report();self.assertIsNone(r['progress']);self.assertEqual(r['partialMean'],.5);self.assertEqual(r['measuredCount'],1)
 def test_math_complete_and_critical(self):
  self.measure('msr_up','kr_up',60);self.measure('msr_down','kr_down',14);self.measure('msr_binary','kr_binary',1)
  r=self.report();self.assertAlmostEqual(r['progress'],2/3);self.assertEqual(r['criticalUnmet'],['kr_up'])
  values={v['id']:v for v in r['keyResults']};self.assertEqual(values['kr_down']['progress'],.5)
 def test_overachievement_regression_and_zero(self):
  self.measure('msr_over','kr_up',100)
  r={x['id']:x for x in self.report()['keyResults']}['kr_up'];self.assertEqual(r['progress'],1);self.assertEqual(r['rawProgress'],1.5)
  self.measure('msr_regress','kr_up',20,day='2026-10-10')
  r={x['id']:x for x in self.report('2026-10-10')['keyResults']}['kr_up'];self.assertEqual(r['progress'],0);self.assertEqual(r['rawProgress'],-.5)
 def test_asof_and_freshness_separate_confidence(self):
  self.measure('msr_early','kr_up',60,day='2026-10-02',confidence=.8)
  self.measure('msr_future','kr_up',80,day='2026-10-20')
  r={x['id']:x for x in self.report('2026-10-19')['keyResults']}['kr_up'];self.assertEqual(r['value'],60);self.assertTrue(r['stale']);self.assertEqual(r['ageDays'],17);self.assertEqual(r['confidence'],.8)
 def test_correction_preserves_history_and_asof(self):
  self.measure('msr_original','kr_up',60,day='2026-10-02')
  self.change([('measurement',dict(id='msr_fix',title='Correction',keyResultId='kr_up',date='2026-10-02',value=64,sourceId='src_test',locator='corrected table',supersedes='msr_original'))],today='2026-10-09')
  old={x['id']:x for x in self.report('2026-10-05')['keyResults']}['kr_up'];self.assertEqual(old['value'],60)
  now={x['id']:x for x in self.report()['keyResults']}['kr_up'];self.assertEqual(now['value'],64)
  self.assertEqual(len(task.load(self.room)[0]['records']['measurement']),2)
 def test_immutable_and_locked_definition(self):
  self.measure('msr_up','kr_up',60)
  for kind,record in [('measurement',dict(id='msr_up',value=70)),('key-result',dict(id='kr_up',target=70))]:
   with self.assertRaises(ValueError):self.change([(kind,record)])
 def test_invalid_metric_evidence_and_binary(self):
  for fields in [dict(target=40),dict(target=20),dict(target=float('nan'))]:
   with self.assertRaises(ValueError):self.change([('key-result',dict(id='kr_up',**fields))])
  for kr,value,extra in [('kr_binary',.5,{}),('kr_up',60,{'sourceId':'src_missing'}),('kr_up',60,{'confidence':2})]:
   r=dict(id='msr_bad',title='Bad',keyResultId=kr,date='2026-10-09',value=value,sourceId='src_test',locator='1');r.update(extra)
   with self.assertRaises(ValueError):self.change([('measurement',r)])
  self.measure('msr_up','kr_up',60)
  with self.assertRaises(ValueError):self.measure('msr_duplicate','kr_up',70)
 def test_task_complete_does_not_measure_kr(self):
  p=task.plan(self.room,[{'op':'complete','id':'tsk_work'}],'agent/test','TEST','2026-10-09');task.apply(self.room,p,p['sha256'])
  self.assertIsNone(self.report()['progress']);self.assertEqual(self.report()['measuredCount'],0)
 def test_review_and_links_html(self):
  self.measure('msr_up','kr_up',60)
  self.change([('review',dict(id='rev_week',title='Weekly',objectiveId='obj_test',date='2026-10-09',obstacles='<script>bad</script>',learnings='Focus on setup',nextTaskIds=['tsk_work']))],today='2026-10-09')
  r=self.report();self.assertEqual(r['reviews'][0]['nextTaskIds'],['tsk_work'])
  html=task.render(task.load(self.room)[0]).decode();self.assertIn('Ziele &amp; Wirkung',html);self.assertIn('table 1',html);self.assertIn('unvollständig',html);self.assertNotIn('<script>bad</script>',html)
  with self.assertRaises(ValueError):self.change([('review',dict(id='rev_bad',title='Bad',objectiveId='obj_test',date='2026-10-09',outcome='achieved'))])
 def test_v1_migration_undo_bundle_and_frozen(self):
  oldroom=self.temp/'old';p=task.legacy_task.init_plan(self.identity,today='2026-10-01');task.legacy_task.apply(oldroom,p,p['sha256'])
  old=task.load(oldroom)[1];original={x.relative_to(oldroom).as_posix():x.read_bytes() for x in oldroom.rglob('*') if x.is_file()}
  bundle=task.export(oldroom);self.assertEqual(bundle['format'],'ai-task-bundle/1')
  p=task.plan(oldroom,[],'agent/test','MIGRATE','2026-10-09');task.apply(oldroom,p,p['sha256']);self.assertEqual(task.load(oldroom)[0]['format'],task.FORMAT)
  for name,contents in original.items():
   if name!='meta/CURRENT':self.assertEqual((oldroom/name).read_bytes(),contents)
  task.verify_generation(oldroom,old)
  p=task.plan(oldroom,[{'op':'undo'}],'agent/test','UNDO','2026-10-09');task.apply(oldroom,p,p['sha256']);self.assertEqual(task.load(oldroom)[0]['records']['objective'],{})
  p=task.import_plan(oldroom,bundle,'agent/test','2026-10-09');task.apply(oldroom,p,p['sha256'])
  destination=self.temp/'frozen';task.freeze(oldroom,destination,'old-compatible');self.assertTrue((destination/'snapshot/state.json').is_file())
 def test_closeout_and_apply_boundary(self):
  self.measure('msr_up','kr_up',60)
  p=task.plan(self.room,[],'agent/test','TEST','2026-10-09')
  p['state']['records']['measurement']['msr_up']['value']=70
  p['sha256']=task.digest({k:v for k,v in p.items() if k!='sha256'})
  before=task.load(self.room)[1]
  with self.assertRaises(ValueError):task.apply(self.room,p,p['sha256'])
  self.assertEqual(task.load(self.room)[1],before)
  self.change([('review',dict(id='rev_close',title='Cycle review',objectiveId='obj_test',date='2026-12-31',reviewType='closeout',outcome='partially-achieved',learnings='Keep measurement method stable')),('objective',dict(id='obj_test',status='closed'))],today='2026-12-31')
  self.assertEqual(self.report('2026-12-31')['reviews'][0]['outcome'],'partially-achieved')
  self.assertEqual(self.report('2026-12-31')['objective']['status'],'closed')
 def test_okr_bundle_roundtrip_cli_and_frozen(self):
  self.measure('msr_up','kr_up',60)
  bundle=task.export(self.room);other=self.temp/'other';p=task.init_plan(self.identity,today='2026-10-09');task.apply(other,p,p['sha256'])
  p=task.import_plan(other,bundle,'agent/test','2026-10-09');task.apply(other,p,p['sha256']);self.assertEqual(task.export(other),bundle)
  result=subprocess.run(['python3',str(ROOT/'ai-task/scripts/task.py'),'okr','--room',str(other),'--today','2026-10-09'],capture_output=True,text=True)
  self.assertEqual(result.returncode,0);self.assertEqual(json.loads(result.stdout)[0]['partialMean'],.5)
  dest=self.temp/'frozen';task.freeze(other,dest,'okr-knowledge');self.assertIn('kr_up',(dest/'snapshot/state.json').read_text())

if __name__=='__main__':unittest.main()
