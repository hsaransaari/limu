from core.builder import *

def Versions():
    return ['2.7.18']

def Build():
    Extract(URL('http://www.python.org/ftp/python/%s/Python-%s.tar.xz' % (Ver(), Ver())))

    Chdir('Python-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
    if Option('link'):
        Execute("ln -s python %s/%s/bin/python2" % (Dest(), Prefix()))
    if Option('virtualenv', 0):
        Chdir(Dest())
        Fetch('virtaulenv.pyz', URL('https://bootstrap.pypa.io/virtualenv/2.7/virtualenv.pyz'))
        Fetch('virtualenv.tar.gz', URL('https://files.pythonhosted.org/packages/68/60/db9f95e6ad456f1872486769c55628c7901fb4de5a72c2f7bdd912abf0c1/virtualenv-20.26.3.tar.gz'))
