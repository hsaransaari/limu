from core.builder import *

def Versions():
    return ['4.9.2']

def Build():
    Extract(URL('http://www.mpfr.org/mpfr-3.1.2/mpfr-3.1.2.tar.gz'))
    Extract(URL('https://gmplib.org/download/gmp/gmp-6.0.0.tar.bz2'))
    Extract(URL('https://ftp.gnu.org/gnu/mpc/mpc-%s.tar.gz' % '1.0.2'))
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%s/gcc-%s.tar.gz' % (Ver(), Ver())))

    Move('mpfr-3.1.2', 'gcc-%s/mpfr' % Ver())
    Execute('mv gmp-6.0.0 gcc-%s/gmp' % Ver())
    Execute('mv mpc-1.0.2 gcc-%s/mpc' % Ver())

    t = Option('target', None)

    Mkdir('build')
    Chdir('build')

    cmd = '../gcc-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    if Option('build_host'):
        cmd += ' --host='+Option('build_host')
#    cmd += ' --with-sysroot=/'
    #cmd += ' --libdir=%s/lib' % Prefix()
    #cmd += ' --libexecdir=%s/libexec' % Prefix()
    #cmd += ' --target=i686-unknown-linux-gnu'

    if not Option('bootstrap', 0):
        cmd += ' --disable-bootstrap'

    cmd += ' --enable-languages=c'
    if Option('cpp', 1):
        cmd += ',c++'

    if not Option('libstdcxx', 1):
        cmd += ' --disable-libstdcxx'
        cmd += ' --disable-libstdcxx-pch'

    if t:
        cmd += ' --target='+t
        cmd += ' --disable-multilib'
        if Option('step') == 1:
            cmd += ' --without-headers'
            cmd += ' --with-newlib'
            cmd += ' --disable-nls'
            cmd += ' --disable-threads'
            cmd += ' --disable-shared'
            cmd += ' --with-glibc-version=2.11'
            cmd += ' --with-local-prefix=%s' % Prefix()
            cmd += ' --with-native-system-header-dir=%s/include' % Prefix()
            cmd += ' --disable-multilib'
            cmd += ' --disable-decimal-float'
            cmd += ' --disable-libatomic'
            cmd += ' --disable-libgomp'
            cmd += ' --disable-libmpx'
            cmd += ' --disable-libquadmath'
            cmd += ' --disable-libssp'
            cmd += ' --disable-libvtv'
            cmd += ' --disable-libstdcxx'
        if Option('step') == 2:
            Execute('export PATH=/sbin:/usr/sbin:/bin:/usr/bin:/tools/bin')
            cmd += ' --host=%s' % t
            cmd += ' --disable-nls'
            cmd += ' --with-local-prefix=%s' % Prefix()
            cmd += ' --with-native-system-header-dir=%s/include' % Prefix()
            cmd += ' --disable-multilib'
            cmd += ' --disable-decimal-float'
            cmd += ' --disable-libatomic'
            cmd += ' --disable-libgomp'
            cmd += ' --disable-libmpx'
            cmd += ' --disable-libquadmath'
            cmd += ' --disable-libssp'
            cmd += ' --disable-libvtv'
            #cmd += ' --disable-libstdcxx'
            #cmd += ' --disable-libstdcxx-pch'

    if Option('sysroot'):
        cmd += ' --with-sysroot=%s' % Option('sysroot')

    if Option('gold', 0):
        cmd += ' --enable-gold=default'

    if not Option('shared', 1):
        cmd += ' --disable-shared'

    if Option('pic', 0):
        cmd += ' --with-pic'
        cmd += ' --enable-host-shared'

    if Option('disable_multilib', 0):
        cmd += ' --disable-multilib'

    if not Option('libquadmath', 1):
        cmd += ' --disable-libquadmath'

    if not Option('libsanitizer', 1):
        cmd += ' --disable-libsanitizer'

    if Option('configure_extra'):
        cmd += ' ' + Option('configure_extra')

    Execute(cmd)
    #if Option('configure_extra'):
    #    Execute('bash')

    if Option('step') == 1:
        #Make('all-gcc')
        #Make('all-target-libgcc')
        #Make('install-gcc DESTDIR='+Dest())
        #Make('install-target-libgcc DESTDIR='+Dest())
        Make()
        Make('install DESTDIR='+Dest())
    else:
        Make()
        Make('install DESTDIR='+Dest())
