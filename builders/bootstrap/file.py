from core.builder import *

def Versions():
    return ['5.30']

def Build():
    Extract(URL('ftp://ftp.astron.com/pub/file/file-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
