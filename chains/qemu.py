# Build qemu and other tools for host

import core, os, sys, platform

versions = {}

def getHostQemu(**params):
    if platform.system() == 'Darwin':
        params.setdefault('fix_osx', 1)
        params.setdefault('kvm', 0)
    else:
        params.setdefault('kvm', 1)

    def b(builder, tools = [], **p):
        p.update(params)
        p.setdefault('version', versions.get(builder, core.getLatestVersion(builder)))
        p.setdefault('host_tool', 1)
        p.setdefault('host_tools', tools)
        return [core.execute('host', builder, p)]

    lpack = b('lpack', use_lpack=0)

    zlib = b('zlib')
    squashfs = b('squashfs', zlib)
    gettext = b('gettext')
    glib = b('glib', gettext + b('libffi') + zlib)
    m4 = b('m4')
    autoconf = b('autoconf', m4)
    automake = b('automake', m4 + autoconf)
    pkg_config = b('pkg_config')
    e2fsprogs = b('e2fsprogs')
    e2tools = b('e2tools', e2fsprogs)
    libarchive = b('libarchive')
    pixman = b('pixman')
    qemu = b('qemu', zlib + gettext + glib + m4 + autoconf + automake + pkg_config + b('libtool', m4) + pixman)
    return qemu + gettext + squashfs + e2fsprogs + e2tools + libarchive

if __name__ == '__main__':
    print getHostQemu()
