from core.builder import *

def Versions():
    return ['0.9.26']

def BuildDependencies():
    return [pkg(), Program('make'), Program('cc'), Program('sh')]

def Provides():
    return [Program('cc'), Program('tcc', Ver())]

def Build():
    Extract(URL('http://download.savannah.nongnu.org/releases/tinycc/tcc-%s.tar.bz2' % Ver()))
    Chdir('tcc-%s' % Ver())
    s = './configure --prefix=%s --cc=cc' % Prefix()
    s += ' --extra-cflags="-static -DCONFIG_TCC_STATIC"'
    Execute(s)
    Make()
    Make('install DESTDIR=%s' % Dest())

    if Option('default_cc'):
        #Mkdir("%s/%s" % (Dest(), Prefix()))
        Chdir("%s/%s" % (Dest(), Prefix()))
        Execute('ln -sf tcc bin/cc')
