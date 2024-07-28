# This chain builds i386 images

import core, os, sys

deterministic = 0

# Versions

versions = { 
    'gcc':           '6.3.0',
    'binutils':      '2.28',
    'glibc':         '2.25',
    #'gcc':           '4.9.4',
    #'binutils':      '2.25',
    #'glibc':         '2.18',
    'bison':         '3.0.4',
    'flex':          '2.5.39',
    'grub':          '2.00',
    'xorriso':       '1.3.8',
    'linux':         '4.10.6',
    'busybox':       '1.26.2',
    'clang':         '3.5.1', # 3.4.2
}

# Helpers

def build(executor, builder_, **params):
    params.setdefault('version', versions.get(builder_, core.getLatestVersion(builder_)))
    print 'executor', executor, 'builder', builder_
    return core.execute(executor, builder_, params)

def buildI386(imagePackage, **params):
    def builder(name, root = [], **p):
        p.update(params)
        p.setdefault('boot', imagePackage)
        p.setdefault('root', root)
        return build('qemu_builder', name, **p)

    kernel_config = []
    #kernel_config = ['40153839']
    #kernel_config = [builder('linux', config=','.join(kernel_config), menuconfig=1)]

    print kernel_config

    binutils = [builder('binutils', gold=1)]
    glibc = [builder('glibc', gold=1)]
    gcc = [builder('gcc', gold=1)]
    make = [builder('make')]
    linuxhdr = [builder('linux', headers=1)]
    busybox = [builder('busybox')]
    toybox = [builder('toybox')]
    limu_base = [builder('limu_base')]

    # More tools, nothing critical anymore.

    bash = [builder('bash', default_sh=1)]

    libarchive = [builder('libarchive')]

    strace = [builder('strace')]
    gawk = [builder('gawk')]
    python = [builder('python')]

    perl = [builder('perl')]
    m4 = [builder('m4')]
    flex = [builder('flex', m4)]
    coreutils = [builder('coreutils')]
    bc = [builder('bc', flex)]

    bison = [builder('bison', m4)]
    grub = [] #builder('grub', m4 + flex + bison)]

    cmake = [builder('cmake')]

    ncurses = [builder('ncurses')]
    vim = [builder('vim')]

    kmod = [builder('kmod')]
    #openssl = [builder('openssl')]
    linux = [builder('linux', [], config=','.join(kernel_config), menuconfig=0)]

    print linux

    xorriso = []#builder('xorriso')]

    zlib = [builder('zlib')]
    squashfs = [builder('squashfs')]

    file = [builder('file')]
    libarchive = [builder('libarchive')]

    pkg_config = [builder('pkg_config')]
    fuse = [builder('fuse')]
    unionfs = [builder('unionfs_fuse', fuse + pkg_config)]

    e2fsprogs = [builder('e2fsprogs', bash, version='1.46.6')]

    #squashfs = [builder('squashfs')]
    gettext = [builder('gettext')]
    libffi = [builder('libffi')]
    glib = [builder('glib', gettext + libffi)]
    #autoconf = [builder('autoconf', m4)]
    #automake = [builder('automake', m4 + autoconf)]
    #libtool = [builder('libtool', m4)]
    #qemu = [builder('qemu', glib + m4 + autoconf + automake + libtool + pkg_config)]

    #curl = [builder('curl', [builder('openssl')])]

    limu_base = [builder('limu_base', initrd=1, builder=1, ext4=0)]

    packages = limu_base + binutils + gcc + glibc + make + gawk + linuxhdr +\
        busybox + bash + strace + python + perl + m4 + flex + coreutils + bc +\
        bison + grub + cmake + ncurses + vim + kmod + linux + xorriso + zlib +\
        squashfs + pkg_config + fuse + unionfs + file + libarchive + e2fsprogs +\
        gettext + libffi + glib

    return (linux, limu_base + busybox + unionfs + linux, packages)
        
def buildI386Image(imagePackage, extras = [], **params):
    def builder(name, root = [], **p):
        p.update(params)
        return build('qemu_builder', name,
            boot=imagePackage,
            root=root,
            **p)

    kernel, boot, root = buildI386(imagePackage, **params)

    img = builder('limu_image', [],
            kernel_package = kernel,
            boot_packages = boot,
            root_packages = root+extras,
            **params)

    return img

if __name__ == '__main__':
    print 'i386 %s' % ','.join(buildI386Image(sys.argv[1]))

#print 'Extracting image hash', img
#os.system('tar xvfz packages/%s.tar.gz' % img)
