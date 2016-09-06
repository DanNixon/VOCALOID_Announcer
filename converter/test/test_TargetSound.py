import unittest
import vocaloid_announcer.types as vat
import test.test_parser as test_parser


class TargetSoundTest(unittest.TestCase):

    def test_TargetSound_invalid(self):
        for s in test_parser.INVALID_SOUND_STRINGS:
            with self.assertRaises(RuntimeError):
                ts = vat.TargetSound(('dummy.wav', s))

    def test_TargetSound_with_3_sound(self):
        data = ('dummy.wav', 'abc...xyz.qqq')
        ts = vat.TargetSound(data)
        parts = ts._components
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[0].name, 'abc')
        self.assertEqual(parts[1].measures, 3)
        self.assertEqual(parts[2].name, 'xyz')
        self.assertEqual(parts[3].measures, 1)
        self.assertEqual(parts[4].name, 'qqq')


if __name__ == '__main__':
    unittest.main()
