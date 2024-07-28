from core.builder import *

def Versions():
    return ['4.9.2']

def lfs_patch():
    Chdir('gcc-%s' % Ver())
    Execute("""for file in \
$(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h)
do
    cp -v $file{,.orig}
    sed -e 's@/lib\(64\)\?\(32\)\?/ld@%s&@g' \
        -e 's@/usr@%s@g' $file.orig > $file
    echo '
#undef STANDARD_STARTFILE_PREFIX_1
#undef STANDARD_STARTFILE_PREFIX_2
#define STANDARD_STARTFILE_PREFIX_1 "%s/lib/"
#define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
    touch $file.orig
done""" % (Prefix(), Prefix(), Prefix()))
    Execute("""sed -i '/k prot/agcc_cv_libc_provides_ssp=yes' gcc/configure""")
    Chdir('..')

def lfs_gcc():
    step = Option('step', 0)

    assert step == 1 or step == 2

    lfs_patch()

    Mkdir('build')
    Chdir('build')
    cmd = '../gcc-%s/configure' % Ver()
    if step == 2:
        c = Option('target')
        cmd = ("CC=%s-gcc CXX=%s-g++ AR=%s-ar RANLIB=%s-ranlib " % (c, c, c, c)) + cmd
        cmd += ' --with-sysroot=%s' % Prefix()
#    cmd += ' --with-gmp='+Prefix()
#    cmd += ' --with-mpfr='+Prefix()
#    cmd += ' --with-mpc='+Prefix()
    cmd += ' --prefix='+Prefix()
    if step == 1:
        cmd += ' --with-local-prefix='+Prefix()
    cmd += ' --with-native-system-header-dir=%s/include' % Prefix()
    cmd += ' --enable-languages=c,c++'

    if step == 1:
        cmd += ' --target='+Option('target')
        cmd += ' --with-sysroot='+Prefix()
        cmd += ' --with-newlib'
        cmd += ' --without-headers'
        cmd += ' --disable-nls'
        cmd += ' --disable-shared'
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
        cmd += ' --disable-libmudflap'

    if step == 2:
        cmd += ' --disable-libstdcxx-pch'
        cmd += ' --disable-multilib'
        cmd += ' --disable-libgomp'

    cmd += ' --disable-bootstrap'

    Execute(cmd)

def Build():
    Extract(URL('http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'))
    Extract(URL('ftp://ftp.gmplib.org/pub/gmp-6.0.0/gmp-6.0.0.tar.bz2'))
    Extract(URL('http://www.multiprecision.org/mpc/download/mpc-1.0.2.tar.gz'))
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    Execute('mv mpfr-3.1.2 gcc-%s/mpfr' % Ver())
    Execute('mv gmp-6.0.0 gcc-%s/gmp' % Ver())
    Execute('mv mpc-1.0.2 gcc-%s/mpc' % Ver())

    lfs_gcc()

    Make()
    Make('install DESTDIR='+Dest())
