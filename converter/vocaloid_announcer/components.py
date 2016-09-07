import re
import logging
from pydub import AudioSegment

LOG = logging.getLogger(__name__)


class SoundComponent(object):
    """
    Base class for components of a target sound.
    """

    def process_audio(self, prev_part, next_part, audio):
        """
        Generates an audio segment for the component.
        @param prev_part Previous audio part
        @param next_part Next audio part
        @param audio Existing audio segment
        @return Tuple of (audio segment, next part offset)
        """
        raise NotImplementedError('No audio processing was implemented')


class AbstractComponentWithDuration(SoundComponent):

    note_div = 0
    measures = 0

    def __init__(self, def_str, type_char):
        super(AbstractComponentWithDuration, self).__init__()

        if len(def_str) < 2:
            raise RuntimeError('Definition string too short')

        if def_str[0] != type_char:
            raise RuntimeError('Incorrect definition')

        parts = def_str[1:].split(':')
        if len(parts) == 1:
            self.note_div = 4
            self.measures = int(parts[0])
        elif len(parts) == 2:
            self.note_div = int(parts[0])
            self.measures = int(parts[1])
        else:
            raise RuntimeError('Unexpected number of parts: %d', len(parts))

    def get_duration_ms(self, resolution = 480):
        quarter_notes = (4.0 / float(self.note_div)) * self.measures
        time_ms = quarter_notes * resolution
        LOG.debug('Pause delay %fms', time_ms)
        return time_ms


class AbstractVSQRegion(SoundComponent):

    name = ''

    def process_audio(self, prev_part, next_part, audio):
        raise RuntimeError('Missing VSQ region "{}"'.format(self.name))

class MissingVSQRegion(AbstractVSQRegion):

    def __init__(self, name):
        super(MissingVSQRegion, self).__init__()
        self.name = name

    def __str__(self):
        return 'MissingVSQRegion("{0}")'.format(self.name)


class Pause(AbstractComponentWithDuration):
    """
    Class representing a pause of a given duration.
    """

    def __init__(self, def_str):
        super(Pause, self).__init__(def_str, '-')

    def process_audio(self, prev_part, next_part, audio):
        return (audio + AudioSegment.silent(duration=self.get_duration_ms()), 0)

    def __str__(self):
        return 'Pause(note_div:{0} measures:{1})'.format(self.note_div, self.measures)


class Crossfade(AbstractComponentWithDuration):
    """
    Class representing a crossfade of a given duration.
    """

    def __init__(self, def_str):
        super(Crossfade, self).__init__(def_str, '^')

    def process_audio(self, prev_part, next_part, audio):
        return (audio.append(next_part.get_audio_snippet(), crossfade=self.get_duration_ms()), 1)

    def __str__(self):
        return 'Crossfade(note_div:{0} measures:{1})'.format(self.note_div, self.measures)


class FadeIn(AbstractComponentWithDuration):
    """
    Class representing a fade in of a given duration.
    """

    def __init__(self, def_str):
        super(FadeIn, self).__init__(def_str, '<')

    def process_audio(self, prev_part, next_part, audio):
        return (audio.append(next_part.get_audio_snippet().fade_in(int(self.get_duration_ms()))), 1)

    def __str__(self):
        return 'FadeIn(note_div:{0} measures:{1})'.format(self.note_div, self.measures)


class FadeOut(AbstractComponentWithDuration):
    """
    Class representing a fade out of a given duration.
    """

    def __init__(self, def_str):
        super(FadeOut, self).__init__(def_str, '>')

    def process_audio(self, prev_part, next_part, audio):
        return (audio.fade_out(int(self.get_duration_ms())), 0)

    def __str__(self):
        return 'FadeOut(note_div:{0} measures:{1})'.format(self.note_div, self.measures)


TYPES = [MissingVSQRegion, Pause, Crossfade, FadeIn, FadeOut]
