from core.builder import *

def Versions():
    return ['327']

def Build():
    Extract(URL('ftp://invisible-island.net/xterm/xterm-%s.tgz' % Ver()))
    Chdir('xterm-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
