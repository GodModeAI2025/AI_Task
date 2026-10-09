import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('task', ROOT / 'ai-task/scripts/task.py')
task = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(task)


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = pathlib.Path(tempfile.mkdtemp(dir=ROOT / 'work'))
        self.room = self.temp / 'room'
        self.identity = {'purpose': 'Synthetic tasks', 'audience': 'Demo', 'language': 'de',
                         'timezone': 'Europe/Berlin', 'tone': 'clear', 'boundaries': 'No invented facts'}
        p = task.init_plan(self.identity)
        task.apply(self.room, p, p['sha256'])

    def tearDown(self):
        shutil.rmtree(self.temp)

    def change(self, actions):
        p = task.plan(self.room, actions, 'agent/test', 'TEST', '2026-10-09')
        task.apply(self.room, p, p['sha256'])
        return p

    def add(self, **fields):
        self.change([{'op': 'upsert', 'kind': 'task', 'record': {'id': 'tsk_one', 'title': 'One', **fields}}])

    def test_SC02_init_identity_and_no_overwrite(self):
        state, generation = task.load(self.room)
        self.assertEqual(state['identity'], self.identity)
        self.assertTrue((self.room / 'meta/generations' / generation / 'SOUL.md').exists())
        p = task.init_plan(self.identity)
        with self.assertRaises(ValueError):
            task.apply(self.room, p, p['sha256'])

    def test_SC03_hierarchy_checklist_and_relations(self):
        self.change([{'op': 'upsert', 'kind': k, 'record': r} for k, r in [
            ('area', {'id': 'area_work', 'title': 'Work'}),
            ('project', {'id': 'prj_demo', 'title': 'Demo', 'areaId': 'area_work'}),
            ('heading', {'id': 'hdg_first', 'title': 'First', 'projectId': 'prj_demo'}),
            ('tag', {'id': 'tag_focus', 'title': 'Focus'}),
            ('task', {'id': 'tsk_one', 'title': 'One', 'listId': 'prj_demo', 'headingId': 'hdg_first',
                      'tags': ['tag_focus'], 'checklist': [{'id': 'chk_one', 'title': 'Read', 'completed': False}]})]])
        self.assertEqual(len(task.query(self.room, 'project', '2026-10-09', 'prj_demo')), 1)
        self.assertEqual(len(task.query(self.room, 'area', '2026-10-09', 'area_work')), 1)
        with self.assertRaises(ValueError):
            self.change([{'op': 'upsert', 'kind': 'task', 'record': {'id': 'tsk_bad', 'title': 'Bad', 'listId': 'prj_missing'}}])

    def test_SC04_stale_and_tampered_plan_zero_writes(self):
        p = task.plan(self.room, [{'op': 'upsert', 'kind': 'task', 'record': {'id': 'tsk_one', 'title': 'One'}}], 'agent/test', 'TEST', '2026-10-09')
        before = (self.room / 'meta/CURRENT').read_bytes()
        altered = copy.deepcopy(p)
        altered['state']['identity']['tone'] = 'tampered'
        with self.assertRaises(ValueError):
            task.apply(self.room, altered, p['sha256'])
        self.assertEqual(before, (self.room / 'meta/CURRENT').read_bytes())
        self.add(title='Other')
        before = (self.room / 'meta/CURRENT').read_bytes()
        with self.assertRaises(ValueError):
            task.apply(self.room, p, p['sha256'])
        self.assertEqual(before, (self.room / 'meta/CURRENT').read_bytes())

    def test_SC04_lock(self):
        p = task.plan(self.room, [], 'agent/test', 'TEST', '2026-10-09')
        (self.room / '.ai-task.lock').mkdir()
        with self.assertRaises(ValueError):
            task.apply(self.room, p, p['sha256'])
        self.assertTrue((self.room / '.ai-task.lock').exists())

    def test_SC05_views_dates_evening(self):
        for ident, fields in [('inbox', {}), ('today', {'status': 'active', 'scheduledDate': '2026-10-08', 'isEvening': True}),
                              ('future', {'status': 'active', 'scheduledDate': '2026-10-10'}),
                              ('deadline', {'status': 'active', 'deadline': '2026-10-08'}),
                              ('someday', {'status': 'active', 'isSomeday': True})]:
            self.change([{'op': 'upsert', 'kind': 'task', 'record': {'id': 'tsk_' + ident, 'title': ident, **fields}}])
        self.assertEqual([x['id'] for x in task.query(self.room, 'inbox', '2026-10-09')], ['tsk_inbox'])
        self.assertEqual({x['id'] for x in task.query(self.room, 'today', '2026-10-09')}, {'tsk_today', 'tsk_deadline'})
        self.assertEqual([x['id'] for x in task.query(self.room, 'upcoming', '2026-10-09')], ['tsk_future'])
        self.assertEqual([x['id'] for x in task.query(self.room, 'someday', '2026-10-09')], ['tsk_someday'])
        with self.assertRaises(ValueError):
            self.add(scheduledDate='2026-02-30')

    def test_SC06_lifecycle_undo(self):
        self.add(status='active')
        self.change([{'op': 'complete', 'id': 'tsk_one'}])
        self.assertEqual(task.query(self.room, 'today', '2026-10-09')[0]['status'], 'completed')
        self.change([{'op': 'log', 'id': 'tsk_one'}])
        self.assertEqual(len(task.query(self.room, 'logbook', '2026-10-09')), 1)
        self.change([{'op': 'trash', 'id': 'tsk_one'}])
        self.assertEqual(len(task.query(self.room, 'trash', '2026-10-09')), 1)
        self.change([{'op': 'restore', 'id': 'tsk_one'}])
        self.assertEqual(task.query(self.room, 'logbook', '2026-10-09')[0]['status'], 'completed')
        self.change([{'op': 'undo'}])
        self.assertEqual(len(task.query(self.room, 'trash', '2026-10-09')), 1)

    def test_SC07_roundtrip_and_unknown_fields(self):
        self.add(notes='Do not translate', status='active')
        bundle = task.export(self.room)
        room2 = self.temp / 'second'
        p = task.init_plan(self.identity)
        task.apply(room2, p, p['sha256'])
        p = task.import_plan(room2, bundle, 'agent/test', '2026-10-09')
        task.apply(room2, p, p['sha256'])
        self.assertEqual(bundle, task.export(room2))
        bundle['records']['task']['tsk_one']['unknown'] = 'preserve or reject'
        with self.assertRaises(ValueError):
            task.import_plan(room2, bundle, 'agent/test', '2026-10-09')

    def test_SC08_repeat_idempotence_month_anchor(self):
        self.add(status='active', isTemplate=True, rrule='FREQ=MONTHLY', nextOccurrence='2026-01-31')
        self.change([{'op': 'tick'}])
        rows = task.query(self.room, 'all', '2026-10-09')
        dates = [x['scheduledDate'] for x in rows]
        self.assertIn('2026-03-31', dates)
        self.assertNotIn('2026-02-28', dates)
        count = len(rows)
        self.change([{'op': 'tick'}])
        self.assertEqual(len(task.query(self.room, 'all', '2026-10-09')), count)
        with self.assertRaises(ValueError):
            self.add(isTemplate=True, rrule='FREQ=YEARLY', nextOccurrence='2026-10-09')

    def test_SC08_weekly_checklist_clone(self):
        self.add(status='active', isTemplate=True, rrule='FREQ=WEEKLY;BYDAY=MO,FR', nextOccurrence='2026-10-05',
                 checklist=[{'id': 'chk_one', 'title': 'Read', 'completed': True}])
        self.change([{'op': 'tick'}])
        rows = task.query(self.room, 'all', '2026-10-09')
        self.assertEqual({x['scheduledDate'] for x in rows}, {'2026-10-05', '2026-10-09'})
        self.assertTrue(all(not x['checklist'][0]['completed'] for x in rows))

    def test_SC09_evidence_search(self):
        self.change([{'op': 'upsert', 'kind': 'source', 'record': {'id': 'src_notes', 'title': 'Meeting', 'reference': 'meeting-export.md', 'text': 'Launch in October'}},
                     {'op': 'upsert', 'kind': 'knowledge', 'record': {'id': 'knw_launch', 'title': 'Launch', 'claims': [{'text': 'Launch in October', 'sourceId': 'src_notes', 'locator': 'line 1'}]}}])
        self.assertEqual(len(task.search(self.room, 'October')), 2)
        with self.assertRaises(ValueError):
            self.change([{'op': 'upsert', 'kind': 'knowledge', 'record': {'id': 'knw_bad', 'title': 'Bad', 'claims': [{'text': 'Invented', 'sourceId': 'src_missing', 'locator': '1'}]}}])

    def test_SC10_manifest_and_html_injection(self):
        self.add(title='<script>alert(1)</script>')
        state, generation = task.load(self.room)
        base = self.room / 'meta/generations' / generation
        html = (base / 'graph/index.html').read_text()
        self.assertNotIn('<script>alert(1)</script>', html)
        self.assertIn('&lt;script&gt;', html)
        record = next((base / 'records/task').glob('*.md'))
        record.write_text('tampered')
        with self.assertRaises(ValueError):
            task.load(self.room)

    def test_SC10_symlink_and_id_traversal(self):
        with self.assertRaises(ValueError):
            self.change([{'op': 'upsert', 'kind': 'task', 'record': {'id': '../bad', 'title': 'Bad'}}])
        (self.room / 'shortcut').symlink_to(self.temp)
        with self.assertRaises(ValueError):
            task.load(self.room)


if __name__ == '__main__':
    (ROOT / 'work').mkdir(exist_ok=True)
    unittest.main()
