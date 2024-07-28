from core.builder import *

def Versions():
    return ['1.4.17']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/m4/m4-%s.tar.xz' % Ver()))
    Chdir('m4-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
