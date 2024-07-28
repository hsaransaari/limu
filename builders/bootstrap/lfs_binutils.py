from core.builder import *

def Versions():
    return ['2.22', '2.24', '2.25']

def BuildDependencies():
    return [pkg(), Program('make'), Program('cc'), Program('sh')]

def Provides():
    return [Program('cc'), Program('binutils', Ver())]

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/binutils/binutils-%s.tar.bz2' % Ver()))
    Mkdir('build')
    Chdir('build')

    step = int(Option('step', 1))
    if step == 1:
        Build1()
    if step == 2:
        Build2()

def Build1():
    cmd = '../binutils-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    cmd += ' --with-sysroot='+Prefix()
    cmd += ' --with-lib-path=%s/lib' % Prefix()
    cmd += ' --target='+Option('target')
    cmd += ' --disable-nls'
    cmd += ' --disable-werror'

    Execute(cmd)
    Make()
    Make('install DESTDIR=%s' % Dest())

    Mkdir('%s/%s' % (Dest(), Prefix()))
    Chdir('%s/%s' % (Dest(), Prefix()))
    Execute('ln -s . tools')

def Build2():
    t = Option('target')

    cmd = "CC=%s-gcc CXX=%s-g++ AR=%s-ar RANLIB=%s-ranlib " % (t, t, t, t)
    cmd += '../binutils-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    cmd += ' --disable-nls'
    cmd += ' --disable-werror'
    cmd += ' --with-lib-path=%s/lib' % Prefix()
    cmd += ' --with-sysroot'

    Execute(cmd)
    Make()
    Make('install DESTDIR=%s' % Dest())

    Make('-C ld clean')
    Make('-C ld LIB_PATH=/usr/lib:/lib')
    Make('cp -v ld/ld-new %s/%s/bin' % (Dest(), Prefix()))

    Mkdir('%s/%s' % (Dest(), Prefix()))
    Chdir('%s/%s' % (Dest(), Prefix()))
    Execute('ln -s . tools')
