from core.builder import *

def Versions():
    return ['9.5.2']

def Build():
    Extract(URL('https://github.com/NetworkConfiguration/dhcpcd/releases/download/v%s/dhcpcd-%s.tar.xz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())

