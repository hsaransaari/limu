from core.builder import *

def Versions():
    return ['0.1']

def Build():
    File('Makefile', open('lpack/Makefile').read())
    File('lpack.c', open('lpack/lpack.c').read())
    Make()
    Mkdir('%s/%s/bin' % (Dest(), Prefix()))
    Execute('cp lpack %s/%s/bin' % (Dest(), Prefix()))
