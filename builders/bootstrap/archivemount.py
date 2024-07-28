from core.builder import *

def Versions():
    return ['0.8.4']

def Build():
    Extract(URL('http://www.cybernoia.de/software/archivemount/archivemount-%s.tar.gz' % Ver()))
    Chdir('%s-%s' % (Builder(), Ver()))
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
