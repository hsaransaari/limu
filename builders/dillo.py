from core.builder import *

def Versions():
    return ['3.1.1']

def Build():
    Extract(URL('https://github.com/dillo-browser/dillo/releases/download/v%s/dillo-%s.tar.bz2' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
