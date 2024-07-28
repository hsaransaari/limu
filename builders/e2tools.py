from core.builder import *

def Versions():
    return ['0.0.16']

def Build():
#    v = Option('e2fsprogs_version', '1.43.4')
#    Extract(URL('https://www.kernel.org/pub/linux/kernel/people/tytso/e2fsprogs/v%s/e2fsprogs-%s.tar.gz' % (v, v)))
#    Chdir('e2fsprogs-%s' % v)
#    Mkdir('build')
#    Chdir('build')
#    Configure()
    #Extract(URL('http://home.earthlink.net/~k_sheff/sw/%s/%s-%s.tar.gz' % (Builder(), Builder(), Ver())))
    #Extract(URL('https://distfiles.alpinelinux.org/distfiles/%s-%s.tar.gz' % (Builder(), Ver())))
    Extract(URL('https://github.com/e2tools/e2tools/releases/download/%s/e2tools-%s.tar.gz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make('LIBS=-lpthread')
    Make('install DESTDIR=%s' % Dest())
