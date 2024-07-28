from core.builder import *

def Versions():
    return ['1.0.2']

def Build():
    #Extract(URL('http://www.multiprecision.org/mpc/download/mpc-%s.tar.gz' % Ver()))
    Extract(URL('https://ftp.gnu.org/gnu/mpc/mpc-%s.tar.gz' % Ver()))

    Mkdir('build')
    Chdir('build')
    cmd = '../mpc-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    cmd += ' --with-gmp='+Prefix()
    cmd += ' --with-mpfr='+Prefix()
    if int(Option('static', 0)):
        cmd += ' --disable-shared --enable-static'
    Execute(cmd)
    Make()

    Make('install DESTDIR='+Dest())
