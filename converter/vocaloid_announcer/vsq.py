import logging
import xmltodict
import json
import os
from vocaloid_announcer.components import AbstractVSQRegion
from pydub import AudioSegment

LOG = logging.getLogger(__name__)


def make_json_paths_absolute(data, json_file):
    """
    Converts the paths in a source sound config file to absolute paths.
    @param data JSON data
    @param json_file Path to JSON file
    """

    json_directory = os.path.abspath(os.path.dirname(json_file))
    for _, s_data in data.iteritems():
        s_data['vsq_file'] = os.path.join(json_directory, s_data['vsq_file'])
        s_data['audio_file'] = os.path.join(json_directory, s_data['audio_file'])


class VSQFileGroup(object):

    files = None

    def __init__(self):
        self.files = list()

    def populate(self, files):
        for f in files:
            file_data = json.load(f)
            make_json_paths_absolute(file_data, f.name)

            for name, data in file_data.iteritems():
                self.files.append(VSQFile(name, data))

    def find(self, name):
        LOG.debug('VSQFileGroup: Finding VSQRegion for name "%s"', name)

        results = []
        for vf in self.files:
            results.extend(vf.find(name))

        if len(results) == 0:
            LOG.warn('No matches found for "%s"', name)

        return results

    def all_region_names(self):
        regions = set()
        for f in self.files:
            regions.update([r.name for r in f.regions])
        return regions

    def __str__(self):
        return 'VSQFileGroup(file count = {})'.format(len(self.files))


class VSQFile(object):

    name = ''
    wav_filename = None
    master_track = None
    tick_start = 0
    regions = None
    ms_per_tick = 0

    def __init__(self, name, data):
        LOG.debug('Loading new VSQFile, name="%s"', name)

        self.name = name
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
        super(VSQRegion, self).__init__()
        self.name = data['name']
        self.data = data
        LOG.debug('New VSQRegion, name=%s', self.name)

    def process_audio(self, prev_part, next_part, audio):
        return (audio + self.get_audio_snippet(), 0)

    def get_audio_snippet(self):
        start_ticks = int(self.data['t']) - self.parent.tick_start
        end_ticks = start_ticks + int(self.data['playTime'])

        start_time_ms = self.parent.ms_per_tick * start_ticks
        end_time_ms = self.parent.ms_per_tick * end_ticks

        LOG.debug('Calculated time %f - %f', start_time_ms, end_time_ms)

        if not os.path.exists(self.parent.wav_filename):
            raise RuntimeError('WAV file not found "%s"', self.parent.wav_filename)

        sound = AudioSegment.from_wav(self.parent.wav_filename)
        return sound[start_time_ms:end_time_ms]

    def resolution(self):
        return int(self.parent.master_track['resolution'])

    def __str__(self):
        return 'VSQRegion("{}")'.format(self.name)
