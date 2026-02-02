import click
from cli.commands.create import create


@click.group()
def cli():
    """FlaskMeridian - Fast Flask setup and automation CLI tool"""
    pass


cli.add_command(create)


if __name__ == '__main__':
    cli()