import logging
import os
from vocaloid_announcer.components import MissingVSQRegion
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
        from vocaloid_announcer.parser import read_json_file
        for f in files:
            data = read_json_file(f)[1]
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
                self.sounds.append(TargetSound(sound[0], sound[1]))
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
                s.process(out_directory, self._metadata['audio_format'], self._metadata.get('pause_note', 4))
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

    def __init__(self, filename, def_str):
        if len(filename) == 0:
            raise RuntimeError('No output filename provided')

        self._filename = filename
        self._components = []

        part_strs = def_str.split()
        if len(part_strs) == 0:
            raise RuntimeError('No definition provided for sound')

        for part in part_strs:
            comp = None

            from vocaloid_announcer.components import TYPES
            for t in TYPES:
                try:
                    comp = t(part)
                    LOG.trace('Found type (%s) for part "%s"', t, part)
                    break
                except:
                    continue

            if comp is None:
                raise RuntimeError('No type found for part "{0}"'.format(part))

            self._components.append(comp)

    def populate_vsq(self, vsq):
        for i, component in enumerate(self._components):
            if isinstance(component, MissingVSQRegion):
                region = vsq.find(component.name)
                if len(region) == 1:
                    self._components[i] = region[0]
                else:
                    LOG.warn('Unexpected number of results for "%s": $d', component.name, len(region))

    def process(self, directory, audio_config, pause_note):
        sound = AudioSegment.empty()

        for i in range(len(self._components)):
            prev_comp = self._components[i - 1] if i - 1 > 0 else None
            next_comp = self._components[i + 1] if i + 1 < len(self._components) else None
            sound, offset = self._components[i].process_audio(prev_comp, next_comp, sound)
            i += offset

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
