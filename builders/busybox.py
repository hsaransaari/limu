from core.builder import *

def Versions():
    return ['1.19.3', '1.22.1', '1.26.2', '1.36.1']

def Build():
    Extract(URL('http://busybox.net/downloads/busybox-%s.tar.bz2' % Ver()))

    if Option('cross'):
        Execute('export CROSS_COMPILE=%s-' % Option('cross'))

    Chdir('busybox-%s' % Ver())
    Execute('make defconfig')
    Prepend('.config', 'CONFIG_STATIC=y')
    # TODO: figure out why is thisa?
    Prepend('.config', 'CONFIG_FEATURE_INETD_RPC=n')
    # Linux 3.19 didn't like depmod from Busybox, better disable mod tools as kmod should be used instead.
    Prepend('.config', 'CONFIG_MODPROBE_SMALL=n')

    #execute('make oldconfig')
    Make()

    if int(Option('no_prefix', 1)):
        Make('CONFIG_PREFIX=%s install' % Dest())
    else:
        Make('CONFIG_PREFIX=%s/%s install' % (Dest(), Prefix()))
