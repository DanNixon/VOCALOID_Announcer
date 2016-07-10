import click
import logging
import converter


class SoundFileData(object):

    def __init__(self):
        self.files = dict()

pass_sound_data = click.make_pass_decorator(SoundFileData, ensure=True)


@click.group()
@click.option('--log-level', default='INFO', help='Logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]')
@click.option('-s', '--sound-file', multiple=True, type=click.File('r'), help='Input sound definition files')
@pass_sound_data
def cli(sound_data, log_level, sound_file):
    """
    File converter for VOCALOID announcer voice banks.
    """
    set_logging(log_level)

    for f in sound_file:
        name, data = converter.read_json_file(f)
        converter.make_json_paths_absolute(data, f.name)
        converter.read_vsq_file(data)
        sound_data.files[name] = data


@cli.command()
@pass_sound_data
def list(sound_data):
    """
    List the sounds available in each input file.
    """
    for name, data in sound_data.files.items():
        click.echo('Sound pack: {0}'.format(name))
        for sound in data['vsq_voice_track']['vsPart']:
            click.echo('\t- {0}'.format(sound['name']))


@cli.command()
@click.argument('output', nargs=-1, type=click.File('r'))
@pass_sound_data
def convert(sound_data, output):
    """
    Creates the voice bank for the specified output files.
    """
    for f in output:
        data = converter.read_json_file(f)[1]
        converter.process_target(data, sound_data.files)


def set_logging(level):
    log_level = getattr(logging, level.upper(), None)
    if not isinstance(log_level, int):
        log_level = logging.INFO

    logging.basicConfig(level=log_level,
                        format='%(levelname)s: %(message)s')
