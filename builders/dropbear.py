from core.builder import *

def Versions():
    return ['2015.67']

def Build():
    Extract(URL('https://matt.ucc.asn.au/dropbear/releases/dropbear-%s.tar.bz2' % Ver()))

    Chdir('dropbear-%s' % Ver())

    c = './configure --prefix=%s' % Prefix()
    c += ' --disable-zlib'
    c += ' --disable-largefile'
    c += ' --disable-loginfunc'
    c += ' --disable-shadow'
    c += ' --disable-utmp'
    c += ' --disable-utmpx'
    c += ' --disable-wtmp'
    c += ' --disable-wtmpx'
    c += ' --disable-pututline'
    c += ' --disable-pututxline'
    c += ' --disable-lastlog'
    Execute(c)
    Make('STATIC=1')
    Make('install DESTDIR=%s' % Dest())
