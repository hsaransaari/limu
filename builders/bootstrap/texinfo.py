from core.builder import *

def Versions():
    return ['5.2']

def Build():
    Extract(URL('http://ftp.gnu.org/gnu/texinfo/texinfo-%s.tar.xz' % Ver()))
    Chdir('texinfo-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR='+Dest())
