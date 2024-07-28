from core.builder import *

def Versions():
    return ['3.00']

def Build():
    Extract(URL('http://sourceforge.net/projects/cdrtools/files/cdrtools-%s.tar.bz2' % Ver()))
    Chdir('cdrtools-%s' % Ver())
    Make()
    Make('INS_BASE=%s/%s install' % (Dest(), Prefix()))
