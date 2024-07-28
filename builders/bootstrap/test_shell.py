from core.builder import *

def Versions():
    return ['0.1']

def Build():
    Execute(Option('sh', 'bash'))
    Execute('exit 1')
