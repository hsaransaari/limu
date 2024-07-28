from core.builder import *

def Versions():
    return ['2.3']

def Build():
    Extract(URL('https://github.com/tmux/tmux/releases/download/%s/tmux-%s.tar.gz' % (Ver(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    Configure()
    Make()
    Make('install DESTDIR=%s' % Dest())

