from core.builder import *

def Versions():
    return ['0.51.0']

def Build():
    Extract(URL('https://launchpad.net/intltool/trunk/%s/+download/intltool-%s.tar.gz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
