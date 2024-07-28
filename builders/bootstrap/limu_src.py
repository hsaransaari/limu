from core.builder import *
import glob

def Versions():
    return ['0.1']

def Build():
    src = []
    src += glob.glob('core/*.py')
    src += glob.glob('executors/*.py')
    src += glob.glob('builders/*.py')

    d = '%s/%s/limu' % (Dest(), Prefix())

    for s in src:
        File('tmp', open(s).read())
        Execute('install -D tmp %s/%s/%s' % (Dest(), Prefix(), s))
