from core.builder import *

def Versions():
    return ['2.21']

def Build():
    Extract(URL('ftp://ftp.gnu.org/gnu/glibc/glibc-%s.tar.xz' % Ver()))
    Chdir('glibc-%s' % Ver())
    Execute("""sed -e '/ia32/s/^/1:/' \
                   -e '/SSE2/s/^1://' \
                   -i sysdeps/i386/i686/multiarch/mempcpy_chk.S""")
    Mkdir('../build')
    Chdir('../build')

    cmd = '../glibc-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    cmd += ' --host='+Option('target')
    cmd += ' --build=$(../glibc-%s/scripts/config.guess)' % Ver()
    cmd += ' --disable-profile'
    cmd += ' --enable-kernel=2.6.32'
    cmd += ' --with-headers=%s/include' % Prefix()
    cmd += ' libc_cv_forced_unwind=yes'
    cmd += ' libc_cv_ctors_header=yes'
    cmd += ' libc_cv_c_cleanup=yes'
    Execute(cmd)

    Make()
    Make('install DESTDIR=%s' % Dest())

    return

    if Option('cross'):
        #cmd = 'CC=%s-gcc ' + cmd
        cmd += ' --host='+Option('cross')
        cmd += ' --build='+Option('cross')
        cmd += ' --enable-obsolete-rpc'

