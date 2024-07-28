from core.builder import *

def Versions():
    return ['1.0.23']

def Build():
    Extract(URL('https://downloads.uclibc-ng.org/releases/%s/uClibc-ng-%s.tar.xz' % (Ver(), Ver())))
    Chdir('uClibc-ng-%s' % Ver())
    Make('defconfig')
    Make()
    Make('install DESTDIR=%s' % Dest())
