import logging
from pydub import AudioSegment

LOG = logging.getLogger(__name__)


def calculate_time(master_track, vocal_part):
    """
    @param master_track
    @param vocal_part
    """

    bpm = int(master_track['tempo'][-1]['v']) / 100.0
    bpq = int(master_track['resolution'])
    ms_per_tick = 60000.0 / (bpm * bpq)
    LOG.debug('Milliseconds per MIDI tick %f', ms_per_tick)

    start_ticks = int(vocal_part['t']) - master_track['_tick_start']
    end_ticks = start_ticks + int(vocal_part['playTime'])

    start_time_ms = ms_per_tick * start_ticks
    end_time_ms = ms_per_tick * end_ticks

    LOG.info('Computed time: %f - %f', start_time_ms, end_time_ms)

    return (start_time_ms, end_time_ms)


def slice_audio(sound_config, audio_config):
    """
    Calculates the timing for a sound file and slices it.
    @param sound_config Configuration data for sound clip
    @param audio_config Configuration for the audio output
    @return The sliced audio segment
    """

    start, end = calculate_time(sound_config[1], sound_config[0])

    sound = AudioSegment.from_wav(sound_config[2])
    sound_segment = sound[start:end]

    sound_segment += audio_config['gain']
    sound_segment = sound_segment.set_channels(audio_config['channels'])
    sound_segment = sound_segment.set_frame_rate(audio_config['sample_freq'])
