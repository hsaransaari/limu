from core.builder import *

def Versions():
    return ['1.15']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/%s/%s-%s.tar.xz' % (Builder(), Builder(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
