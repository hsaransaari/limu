from core.builder import *

def Versions():
    return ['5.9', '6.0']

def Build():
    Extract(URL('http://ftp.gnu.org/gnu//ncurses/ncurses-%s.tar.gz' % Ver()))
    Chdir('ncurses-%s' % Ver())
    cmd = './configure'
    cmd += ' --prefix='+Prefix()
    cmd += ' --with-shared'
    cmd += ' --without-debug'
    cmd += ' --without-ada'
    cmd += ' --enable-widec'
    cmd += ' --enable-overwrite'
    Execute(cmd)
    Make()
    Make('install DESTDIR='+Dest())

    Chdir("%s/%s" % (Dest(), Prefix()))

    Execute('ln -s libncursesw.so lib/libncurses.so')
    Execute('ln -s libncursesw.a  lib/libncurses.a')

    Execute('ln -s libncurses.so  lib/libcurses.so')
    Execute('ln -s libncursesw.so lib/libcursesw.so')
    Execute('ln -s libncurses.a   lib/libcurses.a')
