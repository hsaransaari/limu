from core.builder import *

def Versions():
    return ['3.2.1']

def Build():
    Extract(URL('ftp://sourceware.org/pub/libffi/libffi-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
    d = '%s/%s' % (Dest(), Prefix())
    Mkdir('%s/include' % d)
    Execute('cp %s/lib/libffi-%s/include/* %s/include' % (d, Ver(), d))
