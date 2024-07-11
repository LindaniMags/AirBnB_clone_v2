#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers.
"""

from fabric.api import env, local, put, run
from os.path import exists, isdir
from datetime import datetime
env.hosts = ['52.201.212.72', '54.198.49.42']


def do_pack():
    """generates a .tgz archive from the contents of the web_static"""

    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        archive = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(archive))
        return archive
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""

    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, ext))
        run('rm -rf {}{}/web_static'.format(path, ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, ext))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
