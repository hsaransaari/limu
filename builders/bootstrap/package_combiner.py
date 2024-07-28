from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Mkdir(Dest())
    Chdir(Dest())
    for i in Option('packages').split(','):
        Extract(Package(i))
