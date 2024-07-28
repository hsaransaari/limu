from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Mkdir("%s/%s" % (Dest(), Prefix()))
    Chdir("%s/%s" % (Dest(), Prefix()))
    Execute('ln -s %s %s' % (Option('src'), Option('dst')))
