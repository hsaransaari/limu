from core.builder import *

def Versions():
    return ['8.6.3']

def Build():
    Extract(URL('http://downloads.sourceforge.net/project/tcl/Tcl/%s/tcl%s-src.tar.gz' % (Ver(), Ver())))
    Chdir('tcl%s' % Ver())
    Chdir('unix')
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    #Execute('TZ=UTC make test')
    Make('install DESTDIR='+Dest())
    Make('install-private-headers DESTDIR='+Dest())
    Execute('ln -sv tclsh8.6 %s/%s/bin/tclsh' % (Dest(), Prefix()))
