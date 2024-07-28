from core.builder import *

def Versions():
    #return ['2.1.2', '2.10.1', '2.8.1.1']
    #return ['2.1.2', '2.10.1']
    #return ['2.4.1']
    #return ['2.5.1.1']
    return ['2.12.1']

def Build():
    Provides(Program('qemu', Ver()))
    Extract(URL('https://download.qemu.org/qemu-%s.tar.bz2' % Ver()))
    Chdir('qemu-%s' % Ver())
    if Ver() == '2.5.1.1':
        Execute('sed -i.orig 92s:__OPTIMIZE__:this_is_not_defined: pixman/pixman/pixman-mmx.c')
        Execute('sed -i.orig "s:region-test::" pixman/test/Makefile.sources')
        Execute('sed -i.orig "s:scaling-helpers-test::" pixman/test/Makefile.sources')
    if Option('fix_osx'):
        Execute('sed -i.orig "s:bit_AVX2:(1<<5):" util/bufferiszero.c')
    p = Prefix()
    s = './configure --prefix=%s --target-list=i386-softmmu,x86_64-softmmu' % p

    s += ' --python=python2'

    cflags = "-I%s/include" % p

    if Option('optimize', 1):
        cflags += ' -march=native'
        cflags += ' -O3'
    if Option('kvm', 1):
        s += ' --enable-kvm'
    if Option('xen', 0):
        s += ' --enable-xen'
    if Option('sdl', 0):
        s += ' --enable-sdl'
    if Option('debug', 0):
        s += ' --disable-strip --enable-debug'
    #s += ' --extra-cflags="%s" --extra-ldflags="-L%s/lib"' % (cflags, p)
    s += ' --extra-cflags=-I%s/include --extra-ldflags=-L%s/lib' % (p, p)
    Execute(s)
    Make()
    Make('install DESTDIR=%s' % Dest())
