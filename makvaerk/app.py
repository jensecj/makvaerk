import os
import sys
import json

import click

import planner

import util


@click.group()
def cli():
    pass


@click.command()
@click.argument("host")
@click.argument("config-file")
@click.option("-o", "--out", help="file to save plan into")
def plan(host, config_file, out):
    print(f"planning with {config_file} on {host}")

    plan = planner.plan(host, config_file=config_file)

    sys.stdout.write("plan: ")
    util.print_json(plan)

    if out and not os.path.isdir(out):
        with open(out, "w+") as f:
            json.dump(plan, f, indent=4)

    print("planning complete")


@click.command()
@click.argument("host")
@click.argument("plan-file")
def apply(host, plan_file):
    print(f"applying {plan_file} on {host}")


cli.add_command(plan)
cli.add_command(apply)


if __name__ == "__main__":
    cli()
