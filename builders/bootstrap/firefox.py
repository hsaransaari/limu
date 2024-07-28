from core.builder import *

def Versions():
    return ['39.0']

def Build():
    Extract(URL('https://archive.mozilla.org/pub/firefox/releases/%s/source/firefox-%s.source.tar.bz2' % (Ver(), Ver())))
    #Chdir('%s-%s' % (Builder(), Ver()))
    Mkdir('build')
    Chdir('build')
    #Chdir('mozilla-release')
    Execute('../mozilla-release/configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
