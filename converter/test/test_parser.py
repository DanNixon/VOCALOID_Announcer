import unittest
import vocaloid_announcer.parser as vap

VALID_SOUND_STRINGS = ['aaa', 'aaa.bbb', 'aaa...bbb', 'aaa.bbb..ccc']
INVALID_SOUND_STRINGS = ['', '.', 'aaa.', '.aaa', 'aaa.bbb.']


class TargetSoundStringParserTest(unittest.TestCase):

    def test_validate_valid_strings(self):
        for vs in VALID_SOUND_STRINGS:
            self.assertTrue(vap.validate_target_sound_str(vs))

    def test_validate_invalid_strings(self):
        for ivs in INVALID_SOUND_STRINGS:
            self.assertFalse(vap.validate_target_sound_str(ivs))

    def test_parse_sound_invalid(self):
        for ivs in INVALID_SOUND_STRINGS:
            with self.assertRaises(RuntimeError):
                vap.parse_target_sound_str(ivs)

    def test_parse_sound_simple(self):
        sound_str = 'abc'
        parts = vap.parse_target_sound_str(sound_str)
        self.assertEqual(len(parts), 1)
        self.assertEqual(parts[0]._region_name, 'abc')

    def test_parse_sound_with_2_sound(self):
        sound_str = 'abc...xyz'
        parts = vap.parse_target_sound_str(sound_str)
        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[0]._region_name, 'abc')
        self.assertEqual(parts[1]._measures, 3)
        self.assertEqual(parts[2]._region_name, 'xyz')

    def test_parse_sound_with_3_sound(self):
        sound_str = 'abc...xyz.qqq'
        parts = vap.parse_target_sound_str(sound_str)
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[0]._region_name, 'abc')
        self.assertEqual(parts[1]._measures, 3)
        self.assertEqual(parts[2]._region_name, 'xyz')
        self.assertEqual(parts[3]._measures, 1)
        self.assertEqual(parts[4]._region_name, 'qqq')

if __name__ == '__main__':
    unittest.main()
