from core.builder import *

def Versions():
    return ['0.19.4']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gettext/gettext-%s.tar.xz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
