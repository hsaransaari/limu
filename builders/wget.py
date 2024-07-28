from core.builder import *

def Versions():
    return ['1.15', '1.16.3', '1.17.1', '1.19.1']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/wget/wget-%s.tar.xz' % Ver()))
    Chdir('wget-%s' % Ver())
    Execute('./configure --prefix=%s --with-ssl=openssl' % Prefix())
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
