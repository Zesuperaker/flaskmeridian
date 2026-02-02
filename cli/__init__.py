"""Commands module for FlaskMeridian CLI"""
import click
from flask import Blueprint
from cli.commands.create import create
from cli.commands.auth import auth  # ADD THIS


@click.group()
def cli():
    """FlaskMeridian - Fast Flask setup and automation CLI tool"""
    pass


cli.add_command(create)
cli.add_command(auth)  # ADD THIS


if __name__ == '__main__':
    cli()