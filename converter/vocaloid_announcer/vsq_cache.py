import logging
import xmltodict
import parser

LOG = logging.getLogger(__name__)

SOUND_DATA = {}


def _read_vsq_file(data):
    """
    Reads the VSQ(X) file and stores it along with the JSON.
    @param data JSON data
    """

    LOG.debug('Reading VSQ file %s', data['vsq_file'])
    with open(data['vsq_file'], 'r') as ifp:
        vsq_data = xmltodict.parse(ifp)

        data['vsq_master_track'] = vsq_data['vsq4']['masterTrack']
        data['vsq_voice_track'] = vsq_data['vsq4']['vsTrack']

        # Cache the start timestamp of the first part
        data['vsq_master_track']['_tick_start'] = int(
            vsq_data['vsq4']['vsTrack']['vsPart'][0]['t'])


def read_sound_file(f):
    """
    Reads a VSQ file and adds it to the cache.
    @param f File handle to read from
    """
    name, data = parser.read_json_file(f)
    parser.make_json_paths_absolute(data, f.name)
    _read_vsq_file(data)
    SOUND_DATA[name] = data


def get_sound_data(sound):
    """
    Searches for a retrieves the sound config for a given sound.
    @param sound_name Name of the sound to find
    @return Tuple (VSQ part, VSQ master track, audio filename)
    """

    for f_name, f_data in SOUND_DATA.items():
        for part_data in f_data['vsq_voice_track']['vsPart']:
            name = part_data['name']

            if name == sound_name:
                return (part_data, f_data['vsq_master_track'], f_data['audio_file'])

    raise RuntimeError('Mo data found for sound {}'.format(sound))
