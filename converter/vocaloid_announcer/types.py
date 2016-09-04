import vocaloid_announcer.audio as audio
import vocaloid_announcer.vsq_cache as vsq
import logging
import os
from pydub import AudioSegment

LOG = logging.getLogger(__name__)


class Target(object):
    """
    Stores data and sounds for a single target configuration.
    """

    _metadata = None
    _sounds = []

    def __init__(self, json_data):
        for sound in json_data['sounds'].items():
            try:
                self._sounds.append(TargetSound(sound))
            except RuntimeError as ex:
                LOG.error(ex)

        self._metadata = json_data
        self._metadata.pop('sounds')

    def process(self):
        LOG.info('Processing target %s', self._metadata['profile'])

        # Create output directory
        out_directory = os.path.abspath(self._metadata['directory'])
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        LOG.info('Output directory: %s', out_directory)

        # Create sounds
        for s in self._sounds:
            try:
                s.process(self._metadata['audio_format'])
            except RuntimeError as ex:
                LOG.error(ex)

    def __str__(self):
        return 'Target["{}", {} sound(s)]'.format(self._metadata['profile'], len(self._sounds))


class TargetSound(object):
    """
    Stores sound components for a given target sound.
    """

    _filename = ''
    _components = []

    def __init__(self, json_data):
        self._filename = json_data[0]

        import vocaloid_announcer.parser as parser
        self._components = parser.parse_target_sound_str(json_data[1])

    def process(self, audio_config):
        sound = AudioSegment()

        for component in self._components:
            sound = sound + component.audio()

        sound += audio_config['gain']
        sound = sound.set_channels(audio_config['channels'])
        sound = sound.set_frame_rate(audio_config['sample_freq'])

        sound.export(self._filename, format='wav')

    def __str__(self):
        return 'TargetSound["{}", ({})]'.format(self._filename, ','.join([str(c) for c in self._components]))


class SoundComponent(object):
    """
    Base class for components of a target sound.
    """

    def audio(self):
        """
        Generates an audio segment for the component.
        @return Audio segment
        """
        raise NotImplementedError('No audio conversion was implemented')


class VSQRegion(SoundComponent):
    """
    Class representing a sound component extracted from a region of a VSQ file.
    """

    _region_name = ''

    def __init__(self, name):
        super(SoundComponent, self).__init__()
        self._region_name = name

    def audio(self):
        sound_data = vsq.get_sound_data(self._region_name)
        start, end = audio.calculate_time(sound_data[1], sound_data[0])
        sound = AudioSegment.from_wav(sound_data[2])
        return sound[start:end]

    def __str__(self):
        return 'VSQRegion["{}"]'.format(self._region_name)


class Pause(SoundComponent):
    """
    Class representing a pause of a given number of measures.
    """

    _measures = 0

    def __init__(self, measures):
        super(SoundComponent, self).__init__()
        if type(measures) is str:
            measures = len(measures)
        self._measures = measures

    def audio(self):
        # TODO
        raise NotImplementedError()

    def __str__(self):
        return 'Pause[{} measure(s)]'.format(self._measures)
