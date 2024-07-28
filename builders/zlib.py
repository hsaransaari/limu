from core.builder import *

def Versions():
    return ['1.2.11']

def Build():
    Extract(URL('http://zlib.net/fossils/zlib-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
