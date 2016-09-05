import logging
import xmltodict
import parser
from vocaloid_announcer.types import AbstractVSQRegion

LOG = logging.getLogger(__name__)


class VSQFileGroup(object):

    files = None

    def __init__(self):
        self.files = list()

    def load_file(self, data_file):
        self.files.append(VSQFile(data_file))

    def find(self, name):
        LOG.debug('VSQFileGroup: Finding VSQRegion for name "%s"', name)

        results = []
        for vf in self.files:
            results.extend(vf.find(name))

        if len(results) == 0:
            LOG.warn('No matches found for "%s"', name)

        return results

    def __str__(self):
        return 'VSQFileGroup(file count = {})'.format(len(self.files))


class VSQFile(object):

    name = ''
    wav_filename = None
    master_track = None
    tick_start = 0
    regions = None

    def __init__(self, data_file):
        self.name, data = parser.read_json_file(data_file)
        parser.make_json_paths_absolute(data, data_file.name)

        self.wav_filename = data['audio_file']

        voice_track = None
        with open(data['vsq_file'], 'r') as ifp:
            vsq_data = xmltodict.parse(ifp)

            self.master_track = vsq_data['vsq4']['masterTrack']
            voice_track = vsq_data['vsq4']['vsTrack']

            # Cache the start timestamp of the first part
            self.tick_start = int(voice_track['vsPart'][0]['t'])

        self.regions = []
        for part in voice_track['vsPart']:
            region = VSQRegion(part)
            region.parent = self
            self.regions.append(region)

    def find(self, name):
        LOG.debug('VSQFile: Finding VSQRegion for name "%s"', name)
        return [r for r in self.regions if r.name == name]

    def __str__(self):
        return 'VSQFile("{}", region count = {})'.format(self.name, len(self.regions))


class VSQRegion(AbstractVSQRegion):
    """
    Class representing a sound component extracted from a region of a VSQ file.
    """

    parent = None
    data = None

    def __init__(self, data):
        super(AbstractVSQRegion, self).__init__()
        self.name = data['name']
        self.data = data
        LOG.debug('New VSQRegion, name=%s', self.name)

    def audio(self):
        sound_data = vsq.get_sound_data(self.region_name)
        start, end = audio.calculate_time(self.parent.master_track, self.data)
        sound = AudioSegment.from_wav(self.parent.wav_filename)
        return sound[start:end]

    def __str__(self):
        return 'VSQRegion("{}")'.format(self.name)
