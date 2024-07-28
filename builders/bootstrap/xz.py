from core.builder import *

def Versions():
    return ['5.2.3']

def Build():
    Extract(URL('http://tukaani.org/xz/xz-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
