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
    if Option('build_host'):
        cmd += ' --host='+Option('build_host')

    if Option('cross_target'):
        #cmd = 'CC=%s-gcc ' + cmd
        c = Option('cross_target')
        cmd += ' --host='+c
        cmd += ' --build='+c

    cmd += ' --enable-kernel=2.6.32'
    cmd += ' --disable-profile'
    cmd += ' --enable-obsolete-rpc'

    if not Option('werror', 1):
        cmd += ' --disable-werror'

    if Option('lfs'):
        cmd += ' --host='+Option('target')
        cmd += ' --build=$(../glibc-%s/scripts/config.guess)' % Ver()
        cmd += ' --with-headers=%s/include' % Prefix()
        cmd += ' libc_cv_forced_unwind=yes'
        cmd += ' libc_cv_ctors_header=yes'
        cmd += ' libc_cv_c_cleanup=yes'

    t = Option('target', None)
    if t:
        cmd += ' --build=$MACHTYPE'
        cmd += ' --host='+t
        cmd += ' --target='+t

    if Option('sysroot'):
        cmd += ' --with-headers='+Option('sysroot')+'/include'

    if Option('configure_extra'):
        s += ' ' + Option('configure_extra')

    Execute(cmd)

    Make()
    Make('install DESTDIR=%s' % Dest())
    if Option('sysroot'):
        Chdir(Dest()+'/'+Prefix())
        Execute('ln -sf . %s' % Option('sysroot')[1:])
