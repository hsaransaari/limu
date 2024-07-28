from core.builder import *

def Versions():
    return ['0.5.2', '0.7.3']

def Build():
    Extract(URL('http://www.landley.net/toybox/downloads/toybox-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('make defconfig')
    Execute('CFLAGS=-static make toybox')
    Execute('PREFIX=%s/%s make install' % (Dest(), Prefix()))
    Make()
    Make('install DESTDIR=%s' % Dest())
