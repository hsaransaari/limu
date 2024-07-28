from core.builder import *

def Versions():
    return ['2.05b', '3.2.48', '4.3.30']

def Build():
    Extract(URL('ftp://ftp.gnu.org/gnu/bash/bash-%s.tar.gz' % Ver()))

    Chdir('bash-%s' % Ver())

    if Option('static', 1):
        Configure('--enable-static-link --without-bash-malloc')
    else:
        Configure('--without-bash-malloc')

#    if Option('static'):
#        make('CFLAGS=-static')
#    else:
#        make()

    Make()
#    Make('tests')
    Make('install DESTDIR=%s' % Dest())

    if Option('default_sh', 0):
        Chdir(Dest())
        Mkdir('bin')
        Execute('ln -s %s/bin/bash bin/sh' % Prefix())
        if Prefix() != '/':
            Execute('ln -s %s/bin/bash bin/bash' % Prefix())

    #Execute('ln -s "%s/%s/bin/bash" "%s/%s/../bin/bash"' % (Dest(), Prefix(), Dest(), Prefix()))
