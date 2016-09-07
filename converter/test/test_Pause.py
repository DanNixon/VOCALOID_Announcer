import unittest
from vocaloid_announcer.components import Pause


class PauseTest(unittest.TestCase):

    def test_Pause_str(self):
        c = Pause('-8:3')
        self.assertEquals(8, c.note_div)
        self.assertEquals(3, c.measures)
        self.assertEquals('Pause(note_div:8 measures:3)', str(c))


if __name__ == '__main__':
    unittest.main()
