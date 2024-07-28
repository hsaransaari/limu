from core.builder import *

def pkgname(ver):
    return URL('ftp://sources.redhat.com/pub/newlib/newlib-%s.tar.gz' % ver)

def Versions():
    return ['1.20.0']

def BuildDependencies(ver, opts=[]):
    return [pkgname(ver), Program('make'), Program('cc'), Program('sh')]

def Provides(ver, opts=[]):
    return [Program('libc')]

def Build(ver, opts=[]):
    chdir('newlib-%s' % ver)
    execute('./configure --prefix=/usr --enable-static')
    execute('make -j4')
    execute('make install')
