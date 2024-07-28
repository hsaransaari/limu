from core.builder import *

def Versions():
    return ['4.1.3']

def Build():
    Extract(URL('http://ftp.gnu.org/gnu/gawk/gawk-%s.tar.xz' % Ver()))
    Chdir('gawk-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
