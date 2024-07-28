from core.builder import *

def Versions():
    return ['2.4.75']

def Build():
    Extract(URL('https://dri.freedesktop.org/libdrm/libdrm-%s.tar.gz' % Ver()))
    Chdir('libdrm-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
