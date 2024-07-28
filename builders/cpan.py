from core.builder import *

def Versions():
    return ['none']

def Build():
    a = Option('author')
    p = Option('pkg')
    Extract(URL('http://search.cpan.org/CPAN/authors/id/%s/%s/%s/%s.tar.gz' % (a[0], a[:2], a, p)))
    Chdir('%s' % p)
    Execute('perl Makefile.PL PREFIX=%s DESTDIR=%s' % (Prefix(), Dest()))
    Make()
    Make('test')
    Make('install')
