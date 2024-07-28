from core.builder import *

def Versions():
    return ['0.8.8']

def Build():
    Extract(URL('http://sourceforge.net/projects/docbook2x/files/docbook2x/%s/docbook2X-%s.tar.gz/download' % (Ver(), Ver())))
    Chdir('docbook2X-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
