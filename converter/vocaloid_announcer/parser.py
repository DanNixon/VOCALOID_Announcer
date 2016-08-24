import re
from vocaloid_announcer.types import VSQRegion, Pause

TARGET_SOUND_STR_VALIDATION_REGEX = r'\w+(?:\.+\w+)*$'
SOUND_MATCH_REGEX = r'(\w+)'
PAUSE_MATCH_REGEX = r'(\.+)'


def validate_target_sound_str(sound_str):
    return re.match(TARGET_SOUND_STR_VALIDATION_REGEX, sound_str) is not None


def parse_target_sound_str(sound_str):
    if not validate_target_sound_str(sound_str):
        raise RuntimeError(
            'Target sound string "{}" is not valid'.format(sound_str))

    sound_name_matches = re.findall(SOUND_MATCH_REGEX, sound_str)
    pause_matches = re.findall(PAUSE_MATCH_REGEX, sound_str)

    if len(sound_name_matches) != len(pause_matches) + 1:
        raise RuntimeError('Matched the incorrect number of sound names and pauses ({}, {})'.format(
            len(sound_name_matches), len(pause_matches)))

    sound_parts = [VSQRegion(s) for s in sound_name_matches]
    pause_parts = [Pause(s) for s in pause_matches]

    sound_components = []

    for i in xrange(len(sound_parts)):
        sound_components.append(sound_parts[i])
        if i < len(pause_parts):
            sound_components.append(pause_parts[i])

    return sound_components
