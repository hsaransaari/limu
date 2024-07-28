from core.builder import *

def Versions():
    return ['0.38.0']

def Build():
    Extract(URL('https://www.cairographics.org/releases/pixman-%s.tar.gz' % (Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
