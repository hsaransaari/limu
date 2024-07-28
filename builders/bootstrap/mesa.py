from core.builder import *

def Versions():
    return ['13.0.6']

def Build():
    Extract(URL('ftp://ftp.freedesktop.org/pub/mesa/%s/mesa-%s.tar.gz' % (Ver(), Ver())))
    Chdir('mesa-%s' % Ver())
    Execute('./configure --disable-dri3 --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
