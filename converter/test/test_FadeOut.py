import unittest
from vocaloid_announcer.components import FadeOut


class FadeOutTest(unittest.TestCase):

    def test_FadeOut_str(self):
        f = FadeOut('>8:3')
        self.assertEquals(8, f.note_div)
        self.assertEquals(3, f.measures)
        self.assertEquals('FadeOut(note_div:8 measures:3)', str(f))


if __name__ == '__main__':
    unittest.main()
