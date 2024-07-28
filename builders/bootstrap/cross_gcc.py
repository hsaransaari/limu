from core.builder import *

def Versions():
    return ['4.9.2']

def crossed_gcc():
    lfs_patch()

    Mkdir('build')
    Chdir('build')
    cmd = '../gcc-%s/configure' % Ver()
    cmd += ' --build='+Option('cross')
    cmd += ' --target='+Option('cross')
    cmd += ' --prefix='+Prefix()
    cmd += ' --with-sysroot='+Prefix()
    cmd += ' --with-newlib'
    cmd += ' --without-headers'
    cmd += ' --with-local-prefix='+Prefix()
    cmd += ' --with-native-system-header-dir=%s/include' % Prefix()
    cmd += ' --disable-nls'
    cmd += ' --disable-shared'
    cmd += ' --disable-multilib'
    cmd += ' --disable-decimal-float'
    cmd += ' --disable-threads'
    cmd += ' --disable-libatomic'
    cmd += ' --disable-libgomp'
    cmd += ' --disable-libitm'
    cmd += ' --disable-libquadmath'
    cmd += ' --disable-libsanitizer'
    cmd += ' --disable-libssp'
    cmd += ' --disable-libvtv'
    cmd += ' --disable-libcilkrts'
    cmd += ' --disable-libstdc++-v3'
    cmd += ' --enable-languages=c,c++'
    Execute(cmd)

def Build():
    Extract(URL('http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'))
    Extract(URL('ftp://ftp.gmplib.org/pub/gmp-6.0.0/gmp-6.0.0.tar.bz2'))
    Extract(URL('http://www.multiprecision.org/mpc/download/mpc-1.0.2.tar.gz'))
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    Execute('mv mpfr-3.1.2 gcc-%s/mpfr' % Ver())
    Execute('mv gmp-6.0.0 gcc-%s/gmp' % Ver())
    Execute('mv mpc-1.0.2 gcc-%s/mpc' % Ver())

    #crossed_gcc()
    plain_cross_gcc()

    Make()
    Make('install DESTDIR='+Dest())
