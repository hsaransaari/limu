from core.builder import *

def Versions():
    return ['1.1.29']

def Build():
    Extract(URL('ftp://xmlsoft.org/libxslt/libxslt-%s.tar.gz' % Ver()))
    Chdir('libxslt-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
