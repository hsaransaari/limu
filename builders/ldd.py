from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Fetch('ldd', URL('https://stuff.mit.edu/afs/sipb/project/phone-project/bin/arm-linux-ldd'))
    Execute('chmod +x ldd')
    Mkdir("%s/%s/usr/bin" % (Dest(), Prefix()))
    Copy('ldd', "%s/%s/usr/bin/ldd" % (Dest(), Prefix()))
