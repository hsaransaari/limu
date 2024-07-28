from core.builder import *

def Versions():
    return ['3.3.1']

def Build():
    Extract(URL('https://www.libarchive.org/downloads/libarchive-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
    if Option('default', 1):
        Chdir("%s/%s" % (Dest(), Prefix()))
        Execute('ln -s bsdtar bin/tar')
        Execute('ln -s bsdcpio bin/cpio')
        Execute('ln -s bsdcat bin/cat')
