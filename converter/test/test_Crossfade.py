import unittest
from vocaloid_announcer.components import Crossfade


class CrossfadeTest(unittest.TestCase):

    def test_Crossfade_str(self):
        c = Crossfade('^8:3')
        self.assertEquals(8, c.note_div)
        self.assertEquals(3, c.measures)
        self.assertEquals('Crossfade(note_div:8 measures:3)', str(c))


if __name__ == '__main__':
    unittest.main()
