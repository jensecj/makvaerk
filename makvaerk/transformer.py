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

import configuration

import util


def gather_information(c, ctx):
    print("· gathering information...")
    context = {}

    context.update({"DISTRO": system.distro(c)})
    context.update({"HOSTNAME": system.hostname(c)})

    return context


def pick_package_manager(c, ctx):
    pass


def pre_transform(l, r, ctx):
    print("PRE TRANSFORM")

    gather_information(r, ctx)
    pick_package_manager(r, ctx)

    ctx.update({"TRANSFORM_START_TIME": util.timestamp()})


def _transform(l, r, ctx, config):
    print("TRANSFORM")

    # TODO: do some planning

    # === THE ORDER OF THINGS ===
    # create users
    users = config.get("USERS") or []
    print(f"users = {users}")
    for user in users:
        print(user)
        # print(system.create_user(r, user))

    # create groups
    # add ssh keys
    # add gpg keys
    # set system settings (dont want to disable password login before addins ssh users)
    # transfer files
    # create links
    # install dependencies
    # setup services
    # set app settings


def post_transform(l, r, ctx):
    print("POST TRANSFORM")
    ctx.update({"TRANSFORM_END_TIME": util.timestamp()})


def connect(host):
    remote_config = Config()
    settings = {"hide": True, "warn": True}
    remote_config["sudo"].update(settings)
    remote_config["run"].update(settings)

    if False:  # ignore sudo for now, will be required when working
        sudo_pass = getpass.getpass("sudo password: ")
        remote_config["sudo"].update({"password": sudo_pass})

    return Connection(host, config=remote_config)


def apply(host, config={}, config_file=None):
    if config_file:
        config = configuration.read_from_file(config_file)
        # TODO: load config properly
        # TODO: validate config with json-schema

    local = Context()

    # HACK: use localhost for testing, otherwise fails with no sshd on localhost
    if host == "localhost":
        remote = local
    else:
        remote = connect(host)

    context = {}
    pre_transform(local, remote, context)
    plan = _transform(local, remote, context, config)
    post_transform(local, remote, context)

    sys.stdout.write("context: ")
    util.print_json(context)

    return plan
