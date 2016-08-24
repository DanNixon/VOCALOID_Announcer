import unittest
import vocaloid_announcer.parser as vap


class TargetSoundStringParserTest(unittest.TestCase):

    def test_validate_valid_strings(self):
        strings = ['aaa', 'aaa.bbb', 'aaa...bbb', 'aaa.bbb..ccc']
        for vs in strings:
            self.assertTrue(vap.validate_target_sound_str(vs))

    def test_validate_invalid_strings(self):
        strings = ['', '.', 'aaa.', '.aaa', 'aaa.bbb.']
        for vs in strings:
            print vs
            self.assertFalse(vap.validate_target_sound_str(vs))

    def test_parse_sound_simple(self):
        sound_str = 'abc'
        parts = vap.parse_target_sound_str(sound_str)
        self.assertEquals(len(parts), 1)
        self.assertEquals(parts[0]._region_name, 'abc')

    def test_parse_sound_with_pause(self):
        sound_str = 'abc...xyz'
        parts = vap.parse_target_sound_str(sound_str)
        self.assertEquals(len(parts), 3)
        self.assertEquals(parts[0]._region_name, 'abc')
        self.assertEquals(parts[1]._measures, 3)
        self.assertEquals(parts[2]._region_name, 'xyz')

if __name__ == '__main__':
    unittest.main()
