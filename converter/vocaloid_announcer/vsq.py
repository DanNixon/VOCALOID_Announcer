import logging
import xmltodict
import parser
from vocaloid_announcer.types import AbstractVSQRegion
from pydub import AudioSegment

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
    ms_per_tick = 0

    def __init__(self, data_file):
        self.name, data = parser.read_json_file(data_file)
        parser.make_json_paths_absolute(data, data_file.name)

        self.wav_filename = data['audio_file']

        # Load VSQ tracks
        voice_track = None
        with open(data['vsq_file'], 'r') as ifp:
            vsq_data = xmltodict.parse(ifp)

            self.master_track = vsq_data['vsq4']['masterTrack']
            voice_track = vsq_data['vsq4']['vsTrack']

            # Cache the start timestamp of the first part
            self.tick_start = int(voice_track['vsPart'][0]['t'])

        # Cache ms per MIDI tick
        bpm = int(self.master_track['tempo'][-1]['v']) / 100.0
        ppq = int(self.master_track['resolution'])
        self.ms_per_tick = 60000.0 / (bpm * ppq)
        LOG.debug('Milliseconds per MIDI tick %f', self.ms_per_tick)

        # Parse and add vocal track regions
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

    def audio(self, **args):
        start_ticks = int(self.data['t']) - self.parent.tick_start
        end_ticks = start_ticks + int(self.data['playTime'])

        start_time_ms = self.parent.ms_per_tick * start_ticks
        end_time_ms = self.parent.ms_per_tick * end_ticks

        LOG.debug('Calculated time %f - %f', start_time_ms, end_time_ms)

        sound = AudioSegment.from_wav(self.parent.wav_filename)
        return sound[start_time_ms:end_time_ms]

    def resolution(self):
        return int(self.parent.master_track['resolution'])

    def __str__(self):
        return 'VSQRegion("{}")'.format(self.name)
