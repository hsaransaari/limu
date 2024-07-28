from core.builder import *

def Versions():
    return ['1.15', '1.16.3']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/wget/wget-%s.tar.xz' % Ver()))
    Chdir('wget-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
