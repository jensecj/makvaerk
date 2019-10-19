import os
import sys
import json

import click

import transformer
import util


@click.group()
def cli():
    pass


@click.command()
@click.argument("host")
@click.argument("config-file")
def apply(host, config_file):
    print(f"transforming {host} with {config_file}")
    transformer.apply(host, config_file=config_file)
    print("transformation complete")


cli.add_command(apply)


if __name__ == "__main__":
    cli()
