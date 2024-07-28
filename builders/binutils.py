from core.builder import *

def Versions():
    return ['2.22', '2.24', '2.25']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/binutils/binutils-%s.tar.bz2' % Ver()))
    Mkdir('build')
    Chdir('build')

    t = Option('target', None)

    cmd = '../binutils-%s/configure' % Ver()

    if Option('build_host'):
        cmd += ' --host='+Option('build_host')

    if Option('step') == 2:
        Execute('export PATH=/sbin:/usr/sbin:/bin:/usr/bin:/tools/bin')
        #cmd = "CC=%s-gcc CXX=%s-g++ AR=%s-ar RANLIB=%s-ranlib " % (t, t, t, t) + cmd
        cmd += ' --prefix=/tools --disable-nls --disable-werror --disable-multilib --with-lib-path=/tools/lib --with-sysroot --host=' + t + ' --target=' + t
        #cmd += ' --prefix=/tools --disable-nls --disable-werror --disable-multilib --with-lib-path=/tools/lib --with-sysroot'
        cmd += " CC=%s-gcc CXX=%s-g++ AR=%s-ar RANLIB=%s-ranlib " % (t, t, t, t)
        Execute(cmd)
        Append('Makefile', "MAKEINFO = :")
        #Make('configure-host')
        Make()
        Make('install DESTDIR=%s' % Dest())
        return



    if not t:
        cmd += ' --prefix='+Prefix()
        #cmd += ' --with-sysroot'
        cmd += ' --disable-nls'
        cmd += ' --disable-werror'
    else:
        cmd += ' --prefix='+Prefix()
        cmd += ' --target='+t
        cmd += ' --disable-multilib'
        cmd += ' --disable-nls'
        cmd += ' --disable-werror'

    if Option('gold', 1):
        #cmd += ' --enable-gold=yes --enable-ld=default'
        #cmd += ' --enable-gold=default --disable-ld'
        cmd += ' --enable-gold=yes --enable-ld=yes'
        cmd += ' --enable-plugins'

#    if not Option('multilib', 0):
#        cmd += ' --disable-multilib'

    if Option('sysroot'):
        cmd += ' --with-sysroot=%s' % Option('sysroot')

    if Option('step') == 2:
        cmd += ' --with-lib-path=%s/lib' % Option('sysroot')
        #cmd += ' --host=$MACHTYPE'

#    if not Option('doc', 0):
#        cmd += ' --disable-doc'

    if Option('configure_extra'):
        s += ' ' + Option('configure_extra')

    Execute(cmd)

    if not Option('doc', 0):
        Append('Makefile', "MAKEINFO = :")

    Make('tooldir='+Prefix())
    Make('install DESTDIR=%s' % Dest())
