#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers."""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_pack():
    """Create a compressed archive of your web_static folder."""
    from datetime import datetime
    from fabric.api import local

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(filename))
    if result.failed:
        return None
    return filename


def do_deploy(archive_path):
    """Distribute an archive to your web servers."""
    if not exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    path_no_extension = '/data/web_static/releases/' + filename.split('.')[0]
    put(archive_path, '/tmp/')
    run("mkdir -p {}".format(path_no_extension))
    run("tar -xzf /tmp/{} -C {}".format(filename, path_no_extension))
    run("rm /tmp/{}".format(filename))
    run("mv {}/web_static/* {}".format(path_no_extension, path_no_extension))
    run("rm -rf {}/web_static".format(path_no_extension))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(path_no_extension))
    print("New version deployed!")
    return True


def deploy():
    """Deploy the web_static content."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

