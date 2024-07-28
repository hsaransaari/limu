from core.builder import *

def Versions():
    return ['6.0.0']

def Build():
    Extract(URL('https://gmplib.org/download/gmp/gmp-%s.tar.bz2' % (Ver())))

    Mkdir('build')
    Chdir('build')
    cmd = '../gmp-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    if int(Option('static', 0)):
        cmd += ' --disable-shared --enable-static'
    Execute(cmd)
    Make()

    Make('install DESTDIR='+Dest())
