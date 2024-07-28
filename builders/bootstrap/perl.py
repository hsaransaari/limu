from core.builder import *

def Versions():
    return ['5.20.2']

def Build():
    Extract(URL('http://www.cpan.org/src/5.0/perl-%s.tar.gz' % Ver()))
    Chdir('perl-%s' % Ver())
    Execute('sh Configure -des -Dprefix=%s -Duseshrplib' % Prefix())
    Make('prefix=%s' % Prefix())
    Mkdir(Dest())
    #Execute('mkdir %s/re.0' % Dest())
    #Execute('chmod -rwx %s/re.0' % Dest())
    #Execute('sh')
    Make('install.perl DESTDIR=%s' % Dest())
    #Execute('sh')
    #Mkdir('%s/%s/usr/bin' % (Dest(), Prefix()))
    #Chdir('%s/%s/usr/bin' % (Dest(), Prefix()))
    #Execute('ln -s /bin/perl perl')
