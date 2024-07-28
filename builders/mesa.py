from core.builder import *

def Versions():
    return ['13.0.6']

def Build():
    Extract(URL('https://mesa.freedesktop.org/archive/older-versions/13.x/%s/mesa-%s.tar.gz' % (Ver(), Ver())))
    Chdir('mesa-%s' % Ver())
    Execute('./configure --disable-dri3 --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
