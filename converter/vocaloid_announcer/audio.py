import logging

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
