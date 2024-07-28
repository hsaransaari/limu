from core.builder import *

def Versions():
    return ['1.7.46']

def Build():
    Extract(URL('http://ftp.winehq.org/pub/wine/source/1.7/wine-%s.tar.bz2' % Ver()))

    Chdir('wine-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
