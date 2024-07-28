from core.builder import *

def Versions():
    return ['3.0.4']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/bison/bison-%s.tar.gz' % Ver()))
    Chdir('bison-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
