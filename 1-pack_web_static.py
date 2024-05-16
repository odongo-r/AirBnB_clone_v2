from fabric.api import local
from datetime import datetime

def do_pack():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(dt_string)
    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    return archive_path

