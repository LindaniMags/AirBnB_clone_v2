#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static """
from datetime import datetime
from fabric.api import *

def do_pack():
    """
    making an archive on web_static folder
    """

    date = datetime.now()
    archive = 'web_static_' + date.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    comp = local('tar -cvzf versions/{} web_static'.format(archive))
    if comp is not None:
        return archive
    else:
        return None
