from core.builder import *

def Versions():
    return ['7.53.1']

def Build():
    Extract(URL('https://curl.haxx.se/download/curl-%s.tar.bz2' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
