from core.builder import *

def Versions():
    return ['8.23']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/coreutils/coreutils-%s.tar.xz' % Ver()))

    Chdir('coreutils-%s' % Ver())

    if Option('static'):
        Execute('export LDFLAGS=-static')

    if Option('man_pages', 1):
        Configure()
    else:
        Configure("PERL=")
    Make()
    Make('install DESTDIR=%s' % Dest())
