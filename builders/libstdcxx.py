from core.builder import *

def Versions():
    return ['4.9.2']

def Build():
    #Extract(URL('http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'))
    #Extract(URL('ftp://ftp.gmplib.org/pub/gmp-6.0.0/gmp-6.0.0.tar.bz2'))
    #Extract(URL('http://www.multiprecision.org/mpc/download/mpc-1.0.2.tar.gz'))
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    #Execute('mv mpfr-3.1.2 gcc-%s/mpfr' % Ver())
    #Execute('mv gmp-6.0.0 gcc-%s/gmp' % Ver())
    #Execute('mv mpc-1.0.2 gcc-%s/mpc' % Ver())

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
