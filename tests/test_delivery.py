import concurrent.futures
import importlib.util
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('task_delivery', ROOT / 'ai-task/scripts/task.py')
task = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(task)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'work').mkdir(exist_ok=True)
        self.temp = pathlib.Path(tempfile.mkdtemp(dir=ROOT / 'work'))
        self.room = self.temp / 'room'
        identity = dict(purpose='Synthetic', audience='Demo', language='de', timezone='Europe/Berlin', tone='clear', boundaries='No invented facts')
        p = task.init_plan(identity, today='2026-10-09')
        task.apply(self.room, p, p['sha256'])

    def tearDown(self):
        shutil.rmtree(self.temp)

    def proposal(self, actions):
        return task.plan(self.room, actions, 'agent/test', 'TEST', '2026-10-09')

    def change(self, actions):
        p = self.proposal(actions)
        return task.apply(self.room, p, p['sha256'])

    def test_freeze_is_independent_verified_readonly_snapshot(self):
        self.change([{'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Demo')}])
        frozen = self.temp / 'frozen'
        result = task.freeze(self.room, frozen, 'demo-knowledge')
        self.assertIn('read-only', (frozen / 'SKILL.md').read_text())
        shutil.rmtree(self.room)
        snapshot = json.loads((frozen / 'snapshot/state.json').read_text())
        self.assertEqual(task.digest(snapshot), result['generation'])
        self.assertEqual(snapshot['records']['task']['tsk_demo']['title'], 'Demo')

    def test_simultaneous_apply_has_exactly_one_winner(self):
        p = self.proposal([{'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Demo')}])
        def apply():
            try:
                return task.apply(self.room, p, p['sha256'])['verified']
            except ValueError:
                return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: apply(), range(2)))
        self.assertEqual(results.count(True), 1)
        self.assertEqual(task.load(self.room)[0]['records']['task']['tsk_demo']['title'], 'Demo')

    def test_pointer_failure_leaves_previous_generation_readable(self):
        before = task.load(self.room)[1]
        p = self.proposal([{'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Demo')}])
        with patch.object(task.os, 'replace', side_effect=OSError('synthetic interruption')):
            with self.assertRaises(OSError):
                task.apply(self.room, p, p['sha256'])
        self.assertEqual(task.load(self.room)[1], before)
        self.assertFalse((self.room / '.ai-task.lock').exists())
        task.apply(self.room, p, p['sha256'])
        self.assertNotEqual(task.load(self.room)[1], before)

    def test_project_counts_logged_completion_and_no_implicit_cascade(self):
        self.change([{'op': 'upsert', 'kind': 'project', 'record': dict(id='prj_demo', title='Demo')},
                     {'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Task', status='active', listId='prj_demo')}])
        self.change([{'op': 'complete', 'id': 'tsk_demo'}, {'op': 'log', 'id': 'tsk_demo'}])
        self.assertEqual(len(task.query(self.room, 'project', '2026-10-09', 'prj_demo')), 1)
        with self.assertRaises(ValueError):
            self.proposal([{'op': 'trash', 'kind': 'project', 'id': 'prj_demo'}])
        self.change([{'op': 'complete', 'kind': 'project', 'id': 'prj_demo'}])
        self.assertEqual(len(task.query(self.room, 'logbook', '2026-10-09')), 1)

    def test_cli_errors_do_not_mutate(self):
        before = task.load(self.room)[1]
        result = subprocess.run(['python3', str(ROOT / 'ai-task/scripts/task.py'), 'query', '--room', str(self.room), '--today', 'bad'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(json.loads(result.stderr)['applied'])
        self.assertEqual(task.load(self.room)[1], before)

    def test_recurrence_limits_and_invalid_fields(self):
        with self.assertRaises(ValueError):
            self.proposal([{'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Demo', isTemplate=True, rrule='FREQ=DAILY;COUNT=2', nextOccurrence='2026-10-09')}])
        self.change([{'op': 'upsert', 'kind': 'task', 'record': dict(id='tsk_demo', title='Demo', status='active', isTemplate=True, rrule='FREQ=DAILY', nextOccurrence='2020-01-01')}])
        before = task.load(self.room)[1]
        with self.assertRaises(ValueError):
            self.proposal([{'op': 'tick'}])
        self.assertEqual(task.load(self.room)[1], before)


if __name__ == '__main__':
    unittest.main()
