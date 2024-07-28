from core.builder import *

def Versions():
    return ['7.3', '7.4']

def Build():
    Extract(URL('ftp://ftp.vim.org/pub/vim/unix/vim-%s.tar.bz2' % Ver()))
    Chdir('vim%s' % Ver().replace('.', ''))
    Execute('./configure --prefix=%s --disable-gui --without-x' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
