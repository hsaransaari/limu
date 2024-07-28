from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Mkdir("%s/etc" % (Dest()))
    Chdir("%s/etc" % (Dest()))
    Execute('ldconfig -C ld.so.cache')
