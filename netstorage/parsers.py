import datetime as dt
import os

from .models import NetstorageDiskUsage, NetstorageFile
from lxml import etree


class DirResponse(object):

    def __init__(self, content):
        self.content = content

    def parse(self):
        root = etree.fromstring(self.content)
        root_dir = root.get('directory')
        children = root.getchildren()
        files = [self.build_file(root_dir, child) for child in children]
        return files

    def build_file(self, root, child):
        name = child.get('name')
        path = os.path.join(root, name)
        filetype = child.get('type')
        size = int(child.get('size'))
        mtime = int(child.get('mtime'))
        mtime = dt.datetime.fromtimestamp(mtime)
        md5 = child.get('md5')
        return NetstorageFile(name, filetype, size, mtime, md5, path)


class DuResponse(object):

    def __init__(self, content):
        self.content = content

    def parse(self):
        root = etree.fromstring(self.content)
        path = root.get('directory')
        # du response only contains a single child
        # <du-info files='14986' bytes='694055850'/>
        info = root[0]
        file_count = int(info.get('files'))
        size = int(info.get('bytes'))
        disk_usage = NetstorageDiskUsage(size, file_count, path)
        return disk_usage
