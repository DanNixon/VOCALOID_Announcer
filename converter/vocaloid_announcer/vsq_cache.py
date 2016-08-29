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

    LOG.info('Reading VSQ file %s', data['vsq_file'])
    with open(data['vsq_file'], 'r') as ifp:
        vsq_data = xmltodict.parse(ifp)

        data['vsq_master_track'] = vsq_data['vsq4']['masterTrack']
        data['vsq_voice_track'] = vsq_data['vsq4']['vsTrack']

        # Cache the start timestamp of the first part
        data['vsq_master_track']['_tick_start'] = int(
            vsq_data['vsq4']['vsTrack']['vsPart'][0]['t'])


def read_sound_file(f):
    name, data = parser.read_json_file(f)
    parser.make_json_paths_absolute(data, f.name)
    _read_vsq_file(data)
    SOUND_DATA[name] = data
