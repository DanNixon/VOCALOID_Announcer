import unittest
from vocaloid_announcer.types import Target


class TargetTest(unittest.TestCase):

    def test_Target_parse(self):
        json_data = {
            u'profile': u'profile name goes here',
            u'directory': u'./out/SOUNDS/',
            u'audio_format': {
                u'channels': 1,
                u'sample_freq': 32000,
                u'gain': 22
            },
            u'sounds': {
                u'lap.wav': u'lap_done',
                u'rdiscard.wav': u'race_discarded',
                u'better.wav': u'lap_time_improved',
                u'worse.wav': u'lap_time_regressed',
                u'rsaved.wav': u'race_saved'
            }
        }

        t = Target(json_data)

        self.assertEqual(t._metadata['profile'], u'profile name goes here')
        self.assertEqual(len(t._metadata['audio_format']), 3)
        self.assertEqual(len(t.sounds), 5)

    def test_Target_parse_again(self):
        json_data_1 = {
            u'profile': u'profile name goes here',
            u'directory': u'./out/SOUNDS/',
            u'audio_format': {
                u'channels': 1,
                u'sample_freq': 32000,
                u'gain': 22
            },
            u'sounds': {
                u'lap.wav': u'lap_done',
                u'rdiscard.wav': u'race_discarded',
                u'better.wav': u'lap_time_improved',
                u'worse.wav': u'lap_time_regressed',
                u'rsaved.wav': u'race_saved'
            }
        }

        t1 = Target(json_data_1)

        self.assertEqual(t1._metadata['profile'], u'profile name goes here')
        self.assertEqual(len(t1._metadata['audio_format']), 3)
        self.assertEqual(len(t1.sounds), 5)

        json_data_2 = {
            u'profile': u'second profile name goes here',
            u'directory': u'./out/SOUNDS/en',
            u'audio_format': {
                u'channels': 1,
                u'sample_freq': 32000,
                u'gain': 22
            },
            u'sounds': {
                u'hello.wav': u'hello',
                u'bye.wav': u'bye'
            }
        }

        t2 = Target(json_data_2)

        self.assertEqual(t2._metadata['profile'], u'second profile name goes here')
        self.assertEqual(len(t2._metadata['audio_format']), 3)
        self.assertEqual(len(t2.sounds), 2)


if __name__ == '__main__':
    unittest.main()
