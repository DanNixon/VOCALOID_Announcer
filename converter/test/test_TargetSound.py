import unittest
from vocaloid_announcer.types import TargetSound
from vocaloid_announcer.components import *


class TargetSoundTest(unittest.TestCase):

    def test_TargetSound_invalid_filename_empty(self):
        with self.assertRaises(RuntimeError):
            TargetSound('', 'abc')

    def test_TargetSound_invalid_def_empty(self):
        with self.assertRaises(RuntimeError):
            TargetSound('nope.wav', '')

    def test_TargetSound_1_sound(self):
        s = TargetSound('nope.avi', 'abc')
        self.assertEquals(1, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

    def test_TargetSound_2_sound(self):
        s = TargetSound('nope.avi', 'abc def')
        self.assertEquals(2, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

        self.assertTrue(isinstance(s._components[1], MissingVSQRegion))
        self.assertEquals('def', s._components[1].name)

    def test_TargetSound_2_sound_pause(self):
        s = TargetSound('nope.avi', 'abc -16:8 def')
        self.assertEquals(3, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

        self.assertTrue(isinstance(s._components[1], Pause))
        self.assertEquals(16, s._components[1].note_div)
        self.assertEquals(8, s._components[1].measures)

        self.assertTrue(isinstance(s._components[2], MissingVSQRegion))
        self.assertEquals('def', s._components[2].name)

    def test_TargetSound_2_sound_pause_measures_only(self):
        s = TargetSound('nope.avi', 'abc -8 def')
        self.assertEquals(3, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

        self.assertTrue(isinstance(s._components[1], Pause))
        self.assertEquals(4, s._components[1].note_div)
        self.assertEquals(8, s._components[1].measures)

        self.assertTrue(isinstance(s._components[2], MissingVSQRegion))
        self.assertEquals('def', s._components[2].name)

    def test_TargetSound_2_sound_crossfade(self):
        s = TargetSound('nope.avi', 'abc ^16:8 def')
        self.assertEquals(3, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

        self.assertTrue(isinstance(s._components[1], Crossfade))
        self.assertEquals(16, s._components[1].note_div)
        self.assertEquals(8, s._components[1].measures)

        self.assertTrue(isinstance(s._components[2], MissingVSQRegion))
        self.assertEquals('def', s._components[2].name)

    def test_TargetSound_2_sound_crossfade_measures_only(self):
        s = TargetSound('nope.avi', 'abc ^8 def')
        self.assertEquals(3, len(s._components))

        self.assertTrue(isinstance(s._components[0], MissingVSQRegion))
        self.assertEquals('abc', s._components[0].name)

        self.assertTrue(isinstance(s._components[1], Crossfade))
        self.assertEquals(4, s._components[1].note_div)
        self.assertEquals(8, s._components[1].measures)

        self.assertTrue(isinstance(s._components[2], MissingVSQRegion))
        self.assertEquals('def', s._components[2].name)


if __name__ == '__main__':
    unittest.main()
