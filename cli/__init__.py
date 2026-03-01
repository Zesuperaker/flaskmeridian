"""Commands module for FlaskMeridian CLI"""
import click
from cli.commands.build import build


@click.group()
def cli():
    """FlaskMeridian - Fast Flask setup and automation CLI tool

    🚀 Usage:
        flaskmeridian build        Interactive project builder
    """
    pass


cli.add_command(build)


if __name__ == '__main__':
    cli()