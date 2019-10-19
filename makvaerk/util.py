import os
import sys
import json
import getpass
import datetime
import re

import packaging.version


def timestamp():
    return datetime.datetime.utcnow().isoformat()


def version():
    with open("__version__.py", "r") as f:
        version = f.read().strip()
        match = re.search("^\d+\.\d+\.\d+$", version)

        if not match:
            raise Exception("__version__.py is malformed")

        return version


def version_newer(a, b):
    a = packaging.version.parse(a)
    b = packaging.version.parse(b)
    return a > b


def load_json(file):
    if not os.path.isfile(file):
        return {}

    contents = ""

    with open(file, "r") as f:
        contents = json.load(f)

    return contents or {}


def print_json(j):
    print(json.dumps(j, indent=4))
