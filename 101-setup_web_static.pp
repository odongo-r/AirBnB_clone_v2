#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives."""

from fabric.api import env, local, run
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_clean(number=0):
    """Delete out-of-date archives."""
    number = int(number)
    if number < 1:
        number = 1

    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))

    releases = run("ls -1t /data/web_static/releases").split()
    for release in releases[number:]:
        run("rm -rf /data/web_static/releases/{}".format(release))

