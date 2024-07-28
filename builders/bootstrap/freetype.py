from core.builder import *

def Versions():
    return ['2.7.1']

def Build():
    Extract(URL('http://download.savannah.gnu.org/releases/freetype/freetype-%s.tar.bz2' % Ver()))
    Chdir('freetype-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make('install DESTDIR=%s' % Dest())
