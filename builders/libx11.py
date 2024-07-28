from core.builder import *

def Versions():
    return ['1.5.0']

def Build():
    Extract(URL('https://www.x.org/releases/X11R7.7/src/lib/libX11-%s.tar.bz2' % Ver()))
    Chdir('libX11-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())

