# Install lpack

import core, os, sys, platform

def lpack(**params):
    def b(builder, tools = [], **p):
        p.update(params)
        p.setdefault('host_tool', 1)
        return [core.execute('host', builder, p)]

    lpack = b('lpack', dest=os.getcwd(), prefix="/", produce_package=False)
    os.remove('INSTALL_COMPLETED')

if __name__ == '__main__':
    lpack()

