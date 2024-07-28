from core.builder import *

def Versions():
    return ['1.5.2']

def Build():
    Extract(URL('http://ftp.gnu.org/gnu/dejagnu/dejagnu-%s.tar.gz' % Ver()))
    Chdir('dejagnu-%s' % Ver())
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR='+Dest())
    Make('check')
