from core.builder import *

def Versions():
    return ['6.03']

def Build():
    Extract(URL('https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
