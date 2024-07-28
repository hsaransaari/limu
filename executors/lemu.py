from executors import *
from core.instructions import URL
import builders, core
import sys, os, platform, multiprocessing

def PrepareParams(params):
    params = GenericPrepareParams(params)
    return params

def PrepareInstructions(params, instructions):
    instructions = GenericPrepareInstructions(params, instructions)

    out = []
    out.append(['executor', 'lemu', 0])
    out.extend(instructions)
    #out.append(['execute', 'touch %s/INSTALL_COMPLETED' % params['dest']])
    return out

def Execute(instructions):
    GenericExecute(instructions)

    instructions2 = []

    core.shell.shExec('lemu
-kernel tools/qemu_debian/kernel \
-initrd tools/qemu_debian/initrd')

    #core.shell.mkdir('work/dest')
    #core.shell.shExec('tar xfmo work/result.img -C work/dest')

    return core.packageDirectory('work/dest')

