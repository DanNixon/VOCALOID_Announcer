import unittest
from vocaloid_announcer.components import AbstractComponentWithDuration


class AbstractComponentWithDurationTest(unittest.TestCase):

    def test_AbstractComponentWithDuration_too_many_args(self):
        with self.assertRaises(RuntimeError):
            AbstractComponentWithDuration('-3:3:3', '-')

    def test_AbstractComponentWithDuration_too_few_args(self):
        with self.assertRaises(RuntimeError):
            AbstractComponentWithDuration('-', '-')

    def test_AbstractComponentWithDuration_string_args(self):
        with self.assertRaises(ValueError):
            AbstractComponentWithDuration('-eew:tfs', '-')

    def test_AbstractComponentWithDuration_incorrect_first_char(self):
        with self.assertRaises(RuntimeError):
          AbstractComponentWithDuration('^8:3', '-')

    def test_AbstractComponentWithDuration_measures_only(self):
        c = AbstractComponentWithDuration('-3', '-')
        self.assertEquals(4, c.note_div)
        self.assertEquals(3, c.measures)

    def test_AbstractComponentWithDuration_note_div(self):
        c = AbstractComponentWithDuration('-8:3', '-')
        self.assertEquals(8, c.note_div)
        self.assertEquals(3, c.measures)

    def test_AbstractComponentWithDuration_duration_ms(self):
        c1 = AbstractComponentWithDuration('-4:2', '-')
        self.assertEquals(960, c1.get_duration_ms())
        self.assertEquals(480, c1.get_duration_ms(240))
        c2 = AbstractComponentWithDuration('-8:2', '-')
        self.assertEquals(480, c2.get_duration_ms())
        self.assertEquals(240, c2.get_duration_ms(240))


if __name__ == '__main__':
    unittest.main()
