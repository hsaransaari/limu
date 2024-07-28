from core.builder import *

def Versions():
    return ['2.1.8-stable']

def Build():
    Extract(URL('https://github.com/libevent/libevent/releases/download/release-%s/libevent-%s.tar.gz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
