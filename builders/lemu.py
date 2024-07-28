from core.builder import *

def Versions():
    return ['0.1']

def Build():
    File('Makefile', open('lemu/Makefile').read())
    File('main.cpp', open('lemu/main.cpp').read())
    File('Memory.cpp', open('lemu/Memory.cpp').read())
    File('Memory.hpp', open('lemu/Memory.hpp').read())
    File('ops.c', open('lemu/ops.c').read())
    Make()
    Mkdir('%s/%s/bin' % (Dest(), Prefix()))
    Execute('cp lemu %s/%s/bin' % (Dest(), Prefix()))
