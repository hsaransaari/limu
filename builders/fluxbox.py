from core.builder import *

def Versions():
    return ['1.3.5']

def Build():
    Extract(URL('http://sourceforge.net/projects/fluxbox/files/fluxbox/%s/fluxbox-%s.tar.gz' % (Ver(), Ver())))
    Chdir('fluxbox-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
