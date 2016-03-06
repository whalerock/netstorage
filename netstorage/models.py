from collections import namedtuple


NetstorageFile = namedtuple('NetstorageFile', 'name type size mtime md5 path')
NetstorageDiskUsage = namedtuple('NetstorageDiskUsage', 'size files path')
