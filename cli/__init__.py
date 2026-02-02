"""Commands module for FlaskMeridian CLI"""
import click
from flask import Blueprint
from cli.commands.create import create
from cli.commands.init import init
from cli.commands.auth import auth


@click.group()
def cli():
    """FlaskMeridian - Fast Flask setup and automation CLI tool"""
    pass


cli.add_command(create)
cli.add_command(init)
cli.add_command(auth)


if __name__ == '__main__':
    cli()