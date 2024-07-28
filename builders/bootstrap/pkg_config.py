from core.builder import *

def Versions():
    return ['0.28']

def Build():
    Extract(URL('http://pkgconfig.freedesktop.org/releases/pkg-config-%s.tar.gz' % Ver()))
    Chdir('pkg-config-%s' % Ver())
    Configure('--with-internal-glib')
    Make()
    Make('install DESTDIR=%s' % Dest())
