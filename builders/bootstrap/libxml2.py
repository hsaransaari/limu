from core.builder import *

def Versions():
    return ['2.9.4']

def Build():
    Extract(URL('ftp://xmlsoft.org/libxslt/libxml2-%s.tar.gz' % Ver()))
    Chdir('libxml2-%s' % Ver())
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
