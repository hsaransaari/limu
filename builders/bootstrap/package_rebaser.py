from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Mkdir('tmp')
    Chdir('tmp')
    Extract(Package(Option('package')))
    Chdir('..')
    to = "%s/%s" % (Dest(), Option('dst', '/'))
    Mkdir(to)
    Execute('rmdir %s' % to)
    Move("tmp/%s" % Option('src', '/'), to)
