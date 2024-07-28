from core.builder import *

def Versions():
    return ['1.06']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/bc/bc-%s.tar.gz' % Ver()))
    Chdir('bc-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
