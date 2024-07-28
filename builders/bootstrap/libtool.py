from core.builder import *

def Versions():
    return ['2.4.6']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/%s/%s-%s.tar.xz' % (Builder(), Builder(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
