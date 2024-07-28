from core.builder import *

def Versions():
    return ['1.45.0']

def Build():
    Extract(URL('https://www.kernel.org/pub/linux/kernel/people/tytso/e2fsprogs/v%s/e2fsprogs-%s.tar.gz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure('--disable-nls')
    #Configure('--disable-threads')
    Make()
    Make('install DESTDIR=%s' % Dest())
    if Option('dev_libs', 1):
        Make('install-libs DESTDIR=%s' % Dest())
