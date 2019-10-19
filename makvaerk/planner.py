import os
import sys
import json
import datetime

import getpass

import click

import invoke
from invoke.context import Context
import fabric
from fabric import Config, Connection
from fabrikant import fs, system
from fabrikant.apps import systemd, apt, pacman

import util


def gather_information(c, ctx):
    print("· gathering information...")
    context = {}

    context.update({"DISTRO": system.distro(c)})
    context.update({"HOSTNAME": system.hostname(c)})

    return context


def pick_package_manager(c, ctx):
    pass


def pre_plan(l, r, ctx):
    print("PRE PLAN")

    gather_information(r, ctx)
    pick_package_manager(r, ctx)

    ctx.update({"PLAN_START_TIME": util.timestamp()})


def default_plan():
    return {"version": "1"}


def _plan(l, r, ctx, config):
    print("PLAN")

    plan = default_plan()

    # TODO: do some planning

    return plan


def post_plan(l, r, ctx):
    print("POST PLAN")
    ctx.update({"PLAN_END_TIME": util.timestamp()})


def connect(host):
    remote_config = Config()
    settings = {"hide": True, "warn": True}
    remote_config["sudo"].update(settings)
    remote_config["run"].update(settings)

    if False:  # ignore sudo for now, will be required when working
        sudo_pass = getpass.getpass("sudo password: ")
        remote_config["sudo"].update({"password": sudo_pass})

    return Connection(host, config=remote_config)


def plan(host, config=None, config_file=None):
    if config_file:
        # TODO: load config properly
        # TODO: validate config with json-schema
        config = util.load_json(config_file)

    local = Context()

    # HACK: use localhost for testing, otherwise fails with no sshd on localhost
    if host == "localhost":
        remote = local
    else:
        remote = connect(host)

    context = {}
    pre_plan(local, remote, context)
    plan = _plan(local, remote, context, config)
    post_plan(local, remote, context)

    # TODO: system settings
    # TODO: ssh users
    # TODO: groups
    # TODO: users
    # TODO: dependencies
    # TODO: services
    # TODO: app settings

    sys.stdout.write("context: ")
    util.print_json(context)

    return plan
