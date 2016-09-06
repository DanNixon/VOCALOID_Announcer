import click
import logging
from vocaloid_announcer.types import TargetGroup
from vocaloid_announcer.vsq import VSQFileGroup


INDENT = '  - '


class CLIData(object):

    def __init__(self):
        self.vsq = VSQFileGroup()
        self.target = TargetGroup()

    def populate_vsq(self):
        self.target.populate_vsq(self.vsq)


pass_cli_data = click.make_pass_decorator(CLIData, ensure=True)


@click.group()
@click.option('--log-level', default='INFO', help='Logging level [DEBUG,INFO,WARNING,ERROR,CRITICAL]')
@click.option('-s', '--sound-file', multiple=True, type=click.File('r'), help='Input sound definition files')
@click.option('-t', '--target-file', multiple=True, type=click.File('r'), help='Output target definition files')
@pass_cli_data
def cli(cli_data, log_level, sound_file, target_file):
    """
    File converter for VOCALOID announcer voice banks.
    """
    set_logging(log_level)

    for f in sound_file:
        cli_data.vsq.load_file(f)

    cli_data.target.populate(target_file)


@cli.command()
@pass_cli_data
def list_regions(cli_data):
    """
    List the regions available in each input VSQ file.
    """
    for f in cli_data.vsq.files:
        click.echo('{0}'.format(f))
        for r in f.regions:
            click.echo('{0}{1}'.format(INDENT, r))


@cli.command()
@pass_cli_data
def list_targets(cli_data):
    """
    List the sounds defined in each target.
    """
    for target in cli_data.target.targets:
        click.echo('{0}'.format(target))
        for sound in target.sounds:
            click.echo('{0}{1}'.format(INDENT, sound))


@cli.command()
@pass_cli_data
def list_required_regions(cli_data):
    """
    List the source sounds required to fully generate a target.
    """
    for region in cli_data.target.required_vsq_regions():
        click.echo('{0}'.format(region))


@cli.command()
@pass_cli_data
def list_missing_regions(cli_data):
    """
    List missing source sounds required to fully generate a target.
    """
    cli_data.populate_vsq()
    for region in cli_data.target.missing_vsq_regions():
        click.echo('{0}'.format(region))


@cli.command()
@pass_cli_data
def convert(cli_data):
    """
    Creates the voice bank for the specified output files.
    """
    cli_data.populate_vsq()
    cli_data.target.process()


def set_logging(level):
    log_level = getattr(logging, level.upper(), None)
    if not isinstance(log_level, int):
        log_level = logging.INFO

    logging.basicConfig(level=log_level,
                        format='%(levelname)s: %(message)s')
