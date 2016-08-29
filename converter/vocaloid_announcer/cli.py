import click
import logging
import vsq_cache as vsq


@click.group()
@click.option('--log-level', default='INFO', help='Logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]')
@click.option('-s', '--sound-file', multiple=True, type=click.File('r'), help='Input sound definition files')
def cli(log_level, sound_file):
    """
    File converter for VOCALOID announcer voice banks.
    """
    set_logging(log_level)

    for f in sound_file:
        vsq.read_sound_file(f)


@cli.command()
def list():
    """
    List the sounds available in each input file.
    """
    for name, data in vsq.SOUND_DATA.items():
        click.echo('Sound pack: {0}'.format(name))
        for sound in data['vsq_voice_track']['vsPart']:
            click.echo('\t- {0}'.format(sound['name']))


@cli.command()
@click.argument('output', nargs=-1, type=click.File('r'))
def convert(output):
    """
    Creates the voice bank for the specified output files.
    """
    for f in output:
        # TODO
        pass


def set_logging(level):
    log_level = getattr(logging, level.upper(), None)
    if not isinstance(log_level, int):
        log_level = logging.INFO

    logging.basicConfig(level=log_level,
                        format='%(levelname)s: %(message)s')
