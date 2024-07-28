from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Mkdir(Dest())
    Chdir(Dest())
    Extract(LocalFile(Option('file')))
