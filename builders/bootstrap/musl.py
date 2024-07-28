from core.builder import *

def Versions():
    return ['1.1.7']

def Build():
    Extract(URL('http://www.musl-libc.org/releases/musl-%s.tar.gz' % Ver()))
    Chdir('musl-%s' % Ver())

    cmd = './configure'
    cmd += ' --prefix=%s' % Prefix()
    Execute(cmd)
    Make()
    Make('install DESTDIR=%s' % Dest())
