from core.builder import *

def Versions():
    return ['2.7.9']

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
