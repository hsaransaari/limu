from core.builder import *

def Versions():
    return ['0.34.0']

def Build():
    Extract(URL('https://www.cairographics.org/releases/pixman-%s.tar.gz' % Ver()))
    Chdir('pixman-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
