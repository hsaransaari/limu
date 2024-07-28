from core.builder import *

def Versions():
    return ['1.12.2']

def Build():
    Extract(URL('https://www.x.org/releases/X11R7.7/src/xserver/xorg-server-%s.tar.bz2' % Ver()))
    Chdir('xorg-server-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())

