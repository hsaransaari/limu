from core.builder import *

def Versions():
    return ['3.82']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/make/make-%s.tar.bz2' % Ver()))

    Chdir('make-%s' % Ver())
    Configure()
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
