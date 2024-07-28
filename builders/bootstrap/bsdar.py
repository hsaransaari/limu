from core.builder import *

def Versions():
    return ['1.0.2']

def Build():
    Extract(URL('http://netcologne.dl.sourceforge.net/project/delugebuilds/source/linux/bsdar/bsdar_%s_src.tar.gz' % Ver()))
    Chdir('bsdar')
    Execute('sed -i "s/gcc -s/cc/" Makefile')
    if Option('static'):
        Make('static')
    else:
        Make()
    Execute('cp ar /usr/bin/ar')
