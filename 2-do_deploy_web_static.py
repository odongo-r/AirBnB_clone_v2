#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<web_server_ip_1>', '<web_server_ip_2>']

def do_deploy(archive_path):
    if not exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[-1][:-4]
        run('mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(archive_name, archive_name))
        run('rm /tmp/{}.tgz'.format(archive_name))
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_name, archive_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))
        return True
    except:
        return False
