from core.builder import *

def Versions():
    return ['2.9.7']

def Build():
    Extract(URL('https://github.com/libfuse/libfuse/releases/download/fuse-%s/fuse-%s.tar.gz' % (Ver(), Ver()), 'fuse-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
