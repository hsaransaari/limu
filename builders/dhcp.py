from core.builder import *

def Versions():
    return ['3.1.3']

def Build():
    Extract(URL('ftp://ftp.isc.org/isc/dhcp/dhcp-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())

