from core.builder import *

def Versions():
    return ['2.5.39']

def Build():
    Extract(URL('http://sourceforge.net/projects/flex/files/flex-%s.tar.gz' % Ver()))
    Chdir('flex-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
