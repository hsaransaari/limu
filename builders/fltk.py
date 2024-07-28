from core.builder import *

def Versions():
    return ['1.3.9']

def Build():
    Extract(URL('https://www.fltk.org/pub/fltk/%s/fltk-%s-source.tar.bz2' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())
