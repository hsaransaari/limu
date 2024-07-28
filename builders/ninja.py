from core.builder import *

def Versions():
    return ['1.7.2']

def Build():
    Extract(URL('https://github.com/ninja-build/ninja/archive/v%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
