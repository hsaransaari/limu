from core.builder import *

def Versions():
    return ['2.2.0']

def Build():
    Extract(URL('https://toolchains.bootlin.com/downloads/releases/sources/expat-%s/expat-%s.tar.bz2' % (Ver(), Ver())))
    Chdir('expat-%s' % Ver())
    Execute('./configure --prefix=%s --enable-shared' % Prefix())
    Make('install DESTDIR=%s' % Dest())
