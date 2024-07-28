from core.builder import *

def Versions():
    return ['2.0.34']

def Build():
    Extract(URL('https://downloads.sourceforge.net/acpid2/acpid-%s.tar.xz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
#    Make('install-acpid')

