from core.builder import *

def Versions():
    return ['1.3.8']

def Build():
    Extract(URL('https://www.gnu.org/software/xorriso/xorriso-%s.tar.gz' % Ver()))
    Chdir('xorriso-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
