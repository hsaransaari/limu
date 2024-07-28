from core.builder import *

def Versions():
    return ['1.0']

def Build():
    Extract(URL('http://sourceforge.net/projects/docbook2x/files/docbook2man-sgmlspl/%s/docbook2man-sgmlspl-%s.tar.gz/download' % (Ver(), Ver()),
        'docbook2man-sgmlspl-%s.tar.gz' % Ver()))
    Chdir('docbook2man-sgmlspl-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
