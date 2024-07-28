from core.builder import *

def pkg():
    return URL('ftp://ftp.gnu.org/pub/gnu/tar/tar-%s.tar.bz2' % Ver())

def Versions():
    return ['1.28']

def BuildDependencies():
    return [pkg(), Program('make'), Program('cc'), Program('sh')]

def Provides():
    return [Program('tar'), Program('gtar', Ver())]

def Build():
    chdir('tar-%s' % Ver())
    execute('./configure --prefix=%s' % Prefix())
    make()
    make('install DESTDIR=%s' % Dest())
