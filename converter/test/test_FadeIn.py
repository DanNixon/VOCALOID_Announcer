import unittest
from vocaloid_announcer.components import FadeIn


class FadeInTest(unittest.TestCase):

    def test_FadeIn_str(self):
        f = FadeIn('<8:3')
        self.assertEquals(8, f.note_div)
        self.assertEquals(3, f.measures)
        self.assertEquals('FadeIn(note_div:8 measures:3)', str(f))


if __name__ == '__main__':
    unittest.main()
