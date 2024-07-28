from core.builder import *

def Versions():
    return ['3.7.2']

def Build():
    Extract(URL('https://cmake.org/files/v3.7/cmake-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
