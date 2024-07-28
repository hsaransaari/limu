import os

def Program(name, ver = None):
    return ('program', name, ver)

def URL(url, fn = ''):
    if not fn:
        fn = url.split('/')[-1]
    return ('url', url, fn)

def LocalFile(url, fn = ''):
    url = os.path.abspath(url)
    if not fn:
        fn = url.split('/')[-1]
    return ('file', url, fn)

def Package(h):
    return ('hash', h)
