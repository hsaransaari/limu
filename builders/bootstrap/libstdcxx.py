from core.builder import *

def Versions():
    return ['4.9.4']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    Mkdir('build')
    Chdir('build')
    cmd = '../gcc-%s/libstdc++-v3/configure' % Ver()
    if Option('cross'):
        cmd += ' --build='+Option('cross')
        cmd += ' --host='+Option('cross')
    if Option('step') == 2:
        #cmd += ' --build='+Option('target')
        cmd += ' --host='+Option('target')
    cmd += ' --prefix='+Prefix()
    cmd += ' --disable-multilib'
    #cmd += ' --disable-shared'
    cmd += ' --disable-nls'
    cmd += ' --disable-libstdcxx-threads'
    cmd += ' --disable-libstdcxx-pch'
    if Option('target'):
        cmd += ' --with-gxx-include-dir=/tools/%s/include/c++/%s' % (Option('target'), Ver())
    #cmd += ' --with-gxx-include-dir=%s/%s/include/c++/4.9.2' % (Prefix(), Option('target'))
    Execute(cmd)

    Make()
    Make('install DESTDIR='+Dest())
