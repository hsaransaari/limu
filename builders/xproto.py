from core.builder import *

def Versions():
    return ['7.0.23']

def Build():
    Extract(URL('https://www.x.org/releases/X11R7.7/src/proto/xproto-%s.tar.bz2' % Ver()))
    Chdir('xproto-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
