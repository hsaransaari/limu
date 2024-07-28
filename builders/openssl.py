from core.builder import *

def Versions():
    return ['1.1.1']

def Build():
    Extract(URL('https://www.openssl.org/source/openssl-%s.tar.gz' % Ver()))
    Chdir('openssl-%s' % Ver())
    Execute('./config --prefix=%s' % Prefix())
    Make()
    Make('install_sw install_ssldirs DESTDIR=%s' % Dest())
