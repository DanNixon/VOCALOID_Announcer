import click
import logging
import vocaloid_announcer.vsq_cache as vsq
import vocaloid_announcer.parser as parser
from vocaloid_announcer.types import Target


class TargetData(object):

    def __init__(self):
        self.data = list()

pass_target_data = click.make_pass_decorator(TargetData, ensure=True)


@click.group()
@click.option('--log-level', default='INFO', help='Logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]')
@click.option('-s', '--sound-file', multiple=True, type=click.File('r'), help='Input sound definition files')
@click.option('-t', '--target-file', multiple=True, type=click.File('r'), help='Output target definition files')
@pass_target_data
def cli(target_data, log_level, sound_file, target_file):
    """
    File converter for VOCALOID announcer voice banks.
    """
    set_logging(log_level)

    for f in sound_file:
        vsq.read_sound_file(f)

    for f in target_file:
        data = parser.read_json_file(f)[1]
        target_data.data.append(data)


@cli.command()
def list_sources():
    """
    List the sounds available in each input file.
    """
    for name, data in vsq.SOUND_DATA.items():
        click.echo('Sound pack: {0}'.format(name))
        for sound in data['vsq_voice_track']['vsPart']:
            click.echo('\t- {0}'.format(sound['name']))


@cli.command()
@pass_target_data
def list_targets(target_data):
    """
    List the sounds defined in each target.
    """
    for data in target_data.data:
        target = Target(data)
        click.echo('{0}'.format(target))
        for sound in target.sounds:
            click.echo('\t- {0}'.format(sound))


@cli.command()
@pass_target_data
def convert(target_data):
    """
    Creates the voice bank for the specified output files.
    """
    for data in target_data.dat.data:
        target = Target(data)
        target.process()


def set_logging(level):
    log_level = getattr(logging, level.upper(), None)
    if not isinstance(log_level, int):
        log_level = logging.INFO

    logging.basicConfig(level=log_level,
                        format='%(levelname)s: %(message)s')
