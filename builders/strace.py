from core.builder import *

def Versions():
    return ['4.16']

def Build():
    Extract(URL('https://downloads.sourceforge.net/project/strace/strace/%s/strace-%s.tar.xz' % (Ver(), Ver())))

    Chdir('strace-%s' % Ver())
    Configure()
    if Option('static'):
        Make('LDFLAGS=-static')
    else:
        Make()
    Make('install DESTDIR=%s' % Dest())
