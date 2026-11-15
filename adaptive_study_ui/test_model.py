import unittest
from model import LayoutModel, Session

class ModelTests(unittest.TestCase):
    def test_low_accuracy(self):
        self.assertEqual(LayoutModel().predict(0, 0)[0], 'Support')
    def test_high_accuracy(self):
        self.assertEqual(LayoutModel().predict(1, 0)[0], 'Challenge')
    def test_middle(self):
        self.assertEqual(LayoutModel().predict(.6, .2)[0], 'Standard')
    def test_invalid_input(self):
        with self.assertRaises(ValueError): LayoutModel().predict(2, 0)
    def test_warmup(self):
        s = Session(); s.record(False, False); s.record(False, False)
        self.assertEqual(s.decision()[0], 'Standard')
    def test_errors_change_layout(self):
        s = Session()
        for _ in range(3): s.record(False, False)
        self.assertEqual(s.decision()[0], 'Support')
    def test_success_changes_layout(self):
        s = Session()
        for _ in range(3): s.record(True, False)
        self.assertEqual(s.decision()[0], 'Challenge')
    def test_override_and_resume(self):
        s = Session()
        for _ in range(3): s.record(False, False)
        s.override = 'Challenge'; self.assertEqual(s.decision()[0], 'Challenge')
        s.override = 'Auto'; self.assertEqual(s.decision()[0], 'Support')
    def test_window(self):
        s = Session()
        for _ in range(5): s.record(False, True)
        for _ in range(5): s.record(True, False)
        self.assertEqual(len(s.history), 5)
        self.assertEqual(s.decision()[0], 'Challenge')
    def test_reset_by_new_session(self):
        s = Session(); s.record(True, True)
        self.assertEqual(Session().history, [])

if __name__ == '__main__': unittest.main(verbosity=2)
