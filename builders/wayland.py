from core.builder import *

def Versions():
    return ['2.0.0']

def Build():
    Extract(URL('https://wayland.freedesktop.org/releases/weston-%s.tar.xz' % Ver())

    Chdir('wayland-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
