import logging
import json
import os
import xmltodict
from pydub import AudioSegment


LOG = logging.getLogger(__name__)


def make_json_paths_absolute(data, json_file):
    """
    Converts the paths in a sound config file to absolute paths.
    @param data JSON data
    @param json_file Path to JSON file
    """

    json_directory = os.path.abspath(os.path.dirname(json_file))
    data['vsq_file'] = os.path.join(json_directory, data['vsq_file'])
    data['audio_file'] = os.path.join(json_directory, data['audio_file'])


def read_vsq_file(data):
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


def get_soundfile_config(sound_name, sound_files):
    """
    Searches for a retrieves the sound config for a given sound.
    @param sound_name Name of the sound to find
    @param sound_files All sound files to search through
    @return Tuple (VSQ part, VSQ master track, audio filename)
    """

    for f_name, f_data in sound_files.items():
        for part_data in f_data['vsq_voice_track']['vsPart']:
            name = part_data['name']

            if name == sound_name:
                return (part_data, f_data['vsq_master_track'], f_data['audio_file'])


def process_target(target_config, sound_files):
    """
    Processes audio files for a given target.
    @param target_config Configuration for the target
    @param sound_files Configurations for all sound files
    """

    LOG.info('Processing target %s', target_config['profile'])

    out_directory = os.path.abspath(target_config['directory'])
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)
    LOG.info('Output directory: %s', out_directory)

    for filename, sound_name in target_config['sounds'].items():
        LOG.debug('Processing sound %s', sound_name)
        sound_config = get_soundfile_config(sound_name, sound_files)
        if sound_config is None:
            LOG.warn('Cannot find sound %s', sound_name)
            continue
        out_filename = os.path.join(out_directory, filename)
        slice_audio(sound_config, target_config['audio_format'], out_filename)


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


def slice_audio(sound_config, audio_config, filename):
    """
    Calculates he timing for a sound file, slices it and saves the result.
    @param sound_config Configuration data for sound clip
    @param audio_config Configuration for the audio output
    @param filename Filename of the output audio file
    """

    LOG.info('Processing audio for %s', filename)

    start, end = calculate_time(sound_config[1], sound_config[0])

    sound = AudioSegment.from_wav(sound_config[2])
    sound_segment = sound[start:end]

    sound_segment += audio_config['gain']
    sound_segment = sound_segment.set_channels(audio_config['channels'])
    sound_segment = sound_segment.set_frame_rate(audio_config['sample_freq'])
    sound_segment.export(filename, format='wav')
