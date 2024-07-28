from core.builder import *

def Versions():
    return ['3.12']

def Build():
    Extract(URL('http://kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-%s.tar.bz2' % Ver()))
    Chdir('module-init-tools-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    if Option('manpages', 1):
        Make()
    else:
        Make('DOCBOOKTOMAN=echo')
    Make('install DESTDIR=%s' % Dest())
