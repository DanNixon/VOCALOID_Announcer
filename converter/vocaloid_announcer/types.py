import vocaloid_announcer.audio as audio
import vocaloid_announcer.parser as parser
import logging
import os
from pydub import AudioSegment

LOG = logging.getLogger(__name__)


def _vsq_regions(container, region_type):
    regions = set()
    for sound in container:
        regions.update(getattr(sound, '{0}_vsq_regions'.format(region_type))())
    return regions


class TargetGroup(object):

    def __init__(self):
        self.targets = list()

    def populate(self, files):
        for f in files:
            data = parser.read_json_file(f)[1]
            self.targets.append(Target(data))

    def populate_vsq(self, vsq):
        for targets in self.targets:
            targets.populate_vsq(vsq)

    def process(self):
        for targets in self.targets:
            targets.process()

    def required_vsq_regions(self):
        return _vsq_regions(self.targets, 'required')

    def missing_vsq_regions(self):
        return _vsq_regions(self.targets, 'missing')


class Target(object):
    """
    Stores data and sounds for a single target configuration.
    """

    _metadata = None
    sounds = []

    def __init__(self, json_data):
        for sound in json_data['sounds'].items():
            try:
                self.sounds.append(TargetSound(sound))
            except RuntimeError as ex:
                LOG.error(ex)

        self._metadata = json_data
        self._metadata.pop('sounds')

    def populate_vsq(self, vsq):
        for sound in self.sounds:
            sound.populate_vsq(vsq)

    def process(self):
        LOG.info('Processing target %s', self._metadata['profile'])

        # Create output directory
        out_directory = os.path.abspath(self._metadata['directory'])
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        LOG.info('Output directory: %s', out_directory)

        # Create sounds
        for s in self.sounds:
            try:
                s.process(out_directory, self._metadata['audio_format'])
            except RuntimeError as ex:
                LOG.error(ex)

    def required_vsq_regions(self):
        return _vsq_regions(self.sounds, 'required')

    def missing_vsq_regions(self):
        return _vsq_regions(self.sounds, 'missing')

    def __str__(self):
        return 'Target("{}", {} sound(s))'.format(self._metadata['profile'], len(self.sounds))


class TargetSound(object):
    """
    Stores sound components for a given target sound.
    """

    _filename = ''
    _components = []

    def __init__(self, json_data):
        self._filename = json_data[0]
        self._components = parser.parse_target_sound_str(json_data[1])

    def populate_vsq(self, vsq):
        for i, component in enumerate(self._components):
            if isinstance(component, MissingVSQRegion):
                region = vsq.find(component.name)
                if len(region) == 1:
                    self._components[i] = region[0]

    def process(self, directory, audio_config):
        sound = AudioSegment.empty()

        for component in self._components:
            sound = sound + component.audio()

        sound += audio_config['gain']
        sound = sound.set_channels(audio_config['channels'])
        sound = sound.set_frame_rate(audio_config['sample_freq'])

        filename = os.path.join(directory, self._filename)
        sound.export(filename, format='wav')

    def required_vsq_regions(self):
        return [i.name for i in self._components if isinstance(i, AbstractVSQRegion)]

    def missing_vsq_regions(self):
        return [i.name for i in self._components if isinstance(i, MissingVSQRegion)]

    def __str__(self):
        return 'TargetSound("{}", [{}])'.format(self._filename, ','.join([str(c) for c in self._components]))


class SoundComponent(object):
    """
    Base class for components of a target sound.
    """

    def audio(self):
        """
        Generates an audio segment for the component.
        @return Audio segment
        """
        raise NotImplementedError('No audio generation was implemented')


class AbstractVSQRegion(SoundComponent):

    name = ''


class MissingVSQRegion(AbstractVSQRegion):

    def __init__(self, name):
        super(AbstractVSQRegion, self).__init__()
        self.name = name

    def __str__(self):
        return 'MissingVSQRegion("{0}")'.format(self.name)


class Pause(SoundComponent):
    """
    Class representing a pause of a given number of measures.
    """

    measures = 0

    def __init__(self, measures):
        super(SoundComponent, self).__init__()
        if type(measures) is str:
            measures = len(measures)
        self.measures = measures

    def audio(self):
        # TODO
        raise NotImplementedError()

    def __str__(self):
        return 'Pause({0} measure(s))'.format(self.measures)
