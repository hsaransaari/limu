from core.builder import *

def Versions():
    return ['0.9.14']

def Build():
    Extract(URL('http://sourceforge.net/projects/check/files/check/%s/check-%s.tar.gz' % (Ver(), Ver())))
    Chdir('check-%s' % Ver())
    Execute('PKG_CONFIG= ./configure --prefix=%s' % Prefix())
    Make()
    #Make('check')
    Make('install DESTDIR='+Dest())
