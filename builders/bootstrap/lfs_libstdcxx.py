from core.builder import *

def Versions():
    return ['4.9.4']

def Build():
    Extract(URL('http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'))
    Extract(URL('https://gmplib.org/download/gmp/gmp-6.0.0.tar.bz2'))
    Extract(URL('https://ftp.gnu.org/gnu/mpc/mpc-%s.tar.gz' % '1.0.2'))
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    Execute('mv mpfr-3.1.2 gcc-%s/mpfr' % Ver())
    Execute('mv gmp-6.0.0 gcc-%s/gmp' % Ver())
    Execute('mv mpc-1.0.2 gcc-%s/mpc' % Ver())

    Mkdir('build')
    Chdir('build')
    cmd = '../gcc-%s/libstdc++-v3/configure' % Ver()
    cmd += ' --host='+Option('target')
    cmd += ' --prefix='+Prefix()
    cmd += ' --disable-multilib'
    cmd += ' --disable-shared'
    cmd += ' --disable-nls'
    cmd += ' --disable-libstdcxx-threads'
    cmd += ' --disable-libstdcxx-pch'
    cmd += ' --with-gxx-include-dir=%s/%s/include/c++/%s' % (Prefix(), Option('target'), Ver())
    Execute(cmd)

    Make()
    Make('install DESTDIR='+Dest())
