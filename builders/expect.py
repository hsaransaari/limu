from core.builder import *

def Versions():
    return ['5.45']

def Build():
    Extract(URL('http://prdownloads.sourceforge.net/expect/expect%s.tar.gz' % Ver()))
    Chdir('expect%s' % Ver())
    Execute("cp -v configure configure.orig")
    Execute("sed 's:/usr/local/bin:/bin:' configure.orig > configure")
    Execute('./configure --prefix=%s --with-tcl=%s/lib --with-tclinclude=%s/include' % (Prefix(), Prefix(), Prefix()))
    Make()
    Execute('make test')
    Make('install SCRIPTS="" DESTDIR='+Dest())
