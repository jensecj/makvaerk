import os
import json
import errno

from jsonschema import validate

import util

SCHEMA = {
    "definitions": {
        "user": {
            "type": "object",
            "properties": {
                "group": {"type": "string"},
                "groups": {"type": "array", "items": {"type": "string"}},
                "shell": {"type": "string"},
                "password": {"type": "string"},
            },
        },
        "sshkey": {
            "type": "object",
            "properties": {
                "privatekey": {"type": "string"},
                "publickey": {"type": "string"},
                "name": {"type": "string"},
                "bits": {"type": "number"},
                "sign": {"type": "boolean"},
                "certify": {"type": "boolean"},
                "encrypt": {"type": "boolean"},
                "password": {"type": "string"},
            },
        },
        "file": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "destination": {"type": "string"},
                "file": {"type": "string"},
                "owner": {"type": "string"},
                "executable": {"type": "boolean"},
            },
        },
        "link": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "destination": {"type": "string"},
            },
        },
        "service": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "enabled": {"type": "boolean"},
                "running": {"type": "boolean"},
            },
        },
        # TODO: APP?
        "settings": {
            "type": "object",
            "properties": {
                "password_login": {"type": "boolean"},
                "root_login": {"type": "boolean"},
                "forward_ip4": {"type": "boolean"},
                "nproc_limit": {"type": "number"},
            },
        },
    },
    "type": "object",
    "properties": {
        "GROUPS": {"type": "array", "items": {"type": "string"}},
        "USERS": {"type": "array", "items": {"$ref": "#/definitions/user"}},
        "SSH_KEYS": {"type": "array", "items": {"$ref": "#/definitions/sshkey"}},
        "SETTINGS": {"$ref": "#/definitions/settings"},
        # TODO: rework into TRANSFERS[(src,dst)] + ACCESS[(file,owner,mode)]?
        "FILES": {"type": "array", "items": {"$ref": "#/definitions/file"}},
        # TODO: use [(src,dst)]?
        "LINKS": {"type": "array", "items": {"$ref": "#/definitions/link"}},
        "DEPENDENCIES": {"type": "array", "items": {"type": "string"}},
        "SERVICES": {"type": "array", "items": {"$ref": "#/definitions/service"}},
    },
}


def read_from_file(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

    contents = {}
    with open(file, "r") as f:
        contents.update(json.load(f))

    validate(contents, SCHEMA)

    return contents or {}
