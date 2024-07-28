from core.builder import *

def Versions():
    return ['2.10']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/cpio/cpio-%s.tar.bz2' % Ver()))
    Chdir('cpio-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
