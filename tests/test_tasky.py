import tempfile
import unittest
from pathlib import Path

from tasky.cli import main
from tasky.store import TaskStore


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "tasks.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_assigns_increasing_ids(self):
        s = TaskStore(self.path)
        self.assertEqual(s.add("a").id, 1)
        self.assertEqual(s.add("b").id, 2)

    def test_roundtrip(self):
        s = TaskStore(self.path)
        s.add("write tests")
        s.complete(1)
        s.save()
        loaded = TaskStore(self.path)
        self.assertEqual(len(loaded.tasks), 1)
        self.assertTrue(loaded.tasks[0].done)

    def test_missing_id_raises(self):
        with self.assertRaises(KeyError):
            TaskStore(self.path).complete(42)

    def test_cli_flow(self):
        f = ["--file", str(self.path)]
        self.assertEqual(main(f + ["add", "buy", "milk"]), 0)
        self.assertEqual(main(f + ["done", "1"]), 0)
        self.assertEqual(main(f + ["rm", "9"]), 1)
        self.assertEqual(main(f + ["rm", "1"]), 0)
        self.assertEqual(TaskStore(self.path).tasks, [])


if __name__ == "__main__":
    unittest.main()
