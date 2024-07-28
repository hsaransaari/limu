from core.builder import *

def Versions():
    return ['3.1.2']

def Build():
    Extract(URL('http://www.mpfr.org/mpfr-%s/mpfr-%s.tar.gz' % (Ver(), Ver())))

    Mkdir('build')
    Chdir('build')
    cmd = '../mpfr-%s/configure' % Ver()
    cmd += ' --prefix='+Prefix()
    cmd += ' --with-gmp='+Prefix()
    if int(Option('static', 0)):
        cmd += ' --disable-shared --enable-static'
    Execute(cmd)
    Make()

    Make('install DESTDIR='+Dest())
