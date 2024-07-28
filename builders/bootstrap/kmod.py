from core.builder import *

def Versions():
    return ['20']

def Build():
    Extract(URL('https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
    Chdir("%s/%s" % (Dest(), Prefix()))
    Mkdir('bin')
    Mkdir('sbin')
    for i in 'depmod insmod lsmod modinfo modprobe rmmod'.split():
        Execute('ln -s ../bin/kmod sbin/%s' % i)
    Execute('ln -s kmod bin/lsmod')
