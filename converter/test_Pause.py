import unittest
from vocaloid_announcer.components import Pause


class PauseTest(unittest.TestCase):

    def test_Pause_too_many_args(self):
        with self.assertRaises(RuntimeError):
            Pause('-3:3:3')

    def test_Pause_too_few_args(self):
        with self.assertRaises(RuntimeError):
            Pause('-')

    def test_Pause_string_args(self):
        with self.assertRaises(ValueError):
            Pause('-eew:tfs')

    def test_Pause_incorrect_first_char(self):
        with self.assertRaises(RuntimeError):
          Pause('^8:3')

    def test_Pause_measures_only(self):
        p = Pause('-3')
        self.assertEquals(4, p.note_div)
        self.assertEquals(3, p.measures)

    def test_Pause_note_div(self):
        p = Pause('-8:3')
        self.assertEquals(8, p.note_div)
        self.assertEquals(3, p.measures)


if __name__ == '__main__':
    unittest.main()
