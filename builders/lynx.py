from core.builder import *

def Versions():
    return ['4.9.1']

def Build():
    Extract(URL('
        https://ftp.gnu.org/gnu/screen/screen-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())

