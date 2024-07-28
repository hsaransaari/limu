# This chain builds x86_64 images

import core, os, sys

# Versions

versions = { 
    'gcc':           '6.3.0',
    'binutils':      '2.28',
    'glibc':         '2.25',
    'libstdcxx':     '6.3.0',
    'lfs_gcc':       '4.9.4',
#    'unionfs_fuse':  '2.0',
#    'lfs_binutils':  '2.25',
#    'lfs_glibc':     '2.18',
    'lfs_libstdcxx': '4.9.4',
    'bison':         '3.0.2',
    'flex':          '2.5.39',
    'grub':          '2.00',
    'xorriso':       '1.3.8',
    'linux':         '4.4.68',
    'busybox':       '1.22.1',
    'clang':         '3.9.1', # 3.4.2
#    'glib':          '2.52.1',
}

# Helpers

def build(executor, builder_, **params):
    params.setdefault('version', versions.get(builder_, core.getLatestVersion(builder_)))
    print 'executor', executor, 'builder', builder_
    return core.execute(executor, builder_, params)

def hostTool(name, tools = [], opts = {}):
    return build('host', name, { 'tool': 1, 'host_tools': tools }, opts)

def builder(name, root = [], **opts):
    return build('qemu_builder', name,
        boot=imagePackage,
        root=root,
        **opts)

def rebase(pkg, src = '/', dst = '/'):
    return build('host', 'package_rebaser', package=pkg, src=src, dst=dst)

def crossCompiler(**params):
    target = params['target']
    binutils = [builder('binutils', gold=1, **params)]
    gcc      = [builder('gcc', binutils, step=1, cpp=1, **params)]
    linuxhdr = [builder('linux', headers=1, **params)]
    glibc = [builder('glibc', binutils + gcc + linuxhdr, **params)]
    libstdcxx = []
    libstdcxx = [builder('libstdcxx', binutils + gcc + linuxhdr + glibc, step=2, **params)]

    #binutils2 = [builder('binutils', binutils + gcc + linuxhdr + glibc, step=2, **params)]
    #gcc2      = [builder('gcc', binutils + gcc + linuxhdr + glibc + libstdcxx, step=2, **params)]
    binutils2 = []
    gcc2      = []
    return binutils + gcc + linuxhdr + glibc + libstdcxx + binutils2 + gcc2

def buildFromI386(img, **params):
    global imagePackage
    imagePackage = img

    target = 'x86_64-lfs-linux-gnu'

#    clang = [builder('clang', shared=0, num_threads=1, **params)]

    cc = crossCompiler(target=target, sysroot='/tools', prefix='/tools', **params)
#    gettext = [builder('gettext', cc, build_host=target, **params)]
#    libffi = [builder('libffi', cc, build_host=target, **params)]
#    glib = [builder('glib', cc+gettext+libffi, build_host=target, test=1, **params)]
    fuse = [builder('fuse', cc, build_host=target, prefix='/tools', **params)]
    unionfs = [builder('unionfs_fuse', cc + fuse, cross=target, **params)]

    linuxhdr = [builder('linux', headers=1, prefix='/tools2', **params)]
    glibc2 = [builder('glibc', cc+linuxhdr, build_host=target, multilib=1, sysroot='/tools2', prefix='/tools2', **params)]
    glibc3 = [builder('glibc', cc+linuxhdr, build_host=target, multilib=1, **params)]
    link = [builder('link', src='.', dst='usr', prefix='/tools2', **params)]
    binutils2 = [builder('binutils', cc+linuxhdr+glibc2+link, build_host=target, multilib=1, gold=1, sysroot='/tools2', prefix='/tools2', **params)]
    gcc2 = [builder('gcc', cc+linuxhdr+glibc2+link+binutils2, build_host=target, target=target, cpp=1, multilib=1, shared=1, sysroot='/tools2', prefix='/tools2', configure_extra='--enable-libstdcxx-visibility --with-gnu-as --with-gnu-ld --enable-cxx-flags=-fPIC', pic=1, **params)]

    #cc2 = crossCompiler(target=target, build_host=target, sysroot='/tools2', prefix='/tools2', **params)

    busybox = [builder('busybox', cc, cross=target, version='1.26.2', **params)]
    kmod = [builder('kmod', cc, build_host=target, **params)]
    linux = [builder('linux', cc, arch='x86_64', target=target, cross_target=target, **params)]

    autoconf = [builder('autoconf', cc, build_host=target, **params)]
    automake = [builder('automake', cc + autoconf, build_host=target, **params)]
    make = [builder('make', cc, build_host=target, **params)]
    coreutils = [builder('coreutils', cc, static=0, build_host=target, version='8.21', man_pages=0, **params)]
    gawk = [builder('gawk', cc, build_host=target, **params)]
    strace = [builder('strace', cc, build_host=target, **params)]
    bash = [] #builder('bash', cc, build_host=target, **params)]

    #pkg_config = [builder('pkg_config', cc + glib, build_host=target, **params)]
    m4 = []#builder('m4', cc+glibc3, build_host=target, bash=1, **params)]
    bison = []#builder('bison', cc + glibc3 + m4, build_host=target, **params)]
    file = [builder('file', cc, build_host=target, **params)]

    print params
    limu_base = [builder('limu_base', initrd=1, builder=1, lib64=1, tools2=1, quick_boot=1, **params)]

    kernel = linux
    boot = limu_base + busybox + unionfs + linux
    root = limu_base + busybox + make + coreutils + gawk + strace + bash + m4 + bison + kmod + linux + linuxhdr + glibc2 + link + binutils2 + gcc2 + glibc3 + autoconf + automake + file

    tmpImg = builder('limu_image', [],
            kernel_package = kernel,
            boot_packages = boot,
            root_packages = root,
            **params)

    imagePackage = tmpImg

    params['qemu_arch'] = 'x86_64'
    #libc = [builder('uclibc_ng', **params)]

    make = [builder('make', **params)]

    gcc = [builder('gcc', hack=0, bootstrap=0, gold=0, cpp=1, shared=1, libstdcxx=1, libquadmath=1, libsanitizer=1, pic=1, disable_multilib=1, **params)]
    binutils = [builder('binutils', gold=0, doc=1, version='2.26', **params)]
    linuxhdr = [builder('linux', headers=1, **params)]
    glibc = [builder('glibc', linuxhdr, gold=0, **params)]

    busybox = [builder('busybox', version='1.26.2', **params)]
    kmod = [builder('kmod', **params)]
    m4 = [builder('m4', **params)]
    flex = [builder('flex', m4, **params)]
    bc = [builder('bc', flex, **params)]
    link = [builder('link', src='gcc', dst='cc', prefix='/usr/bin', **params)]
    perl = [builder('perl', gcc+binutils+glibc, **params)]
    openssl = [builder('openssl', perl, **params)]
    linux = [builder('linux', bc + openssl + perl, **params)]

    pkg_config = [builder('pkg_config', **params)]
    fuse = [builder('fuse', **params)]
    unionfs = [builder('unionfs_fuse', fuse + pkg_config + gcc+binutils+glibc, **params)]

    zlib = [builder('zlib', gcc+binutils+glibc, **params)]
    squashfs = [builder('squashfs', zlib+gcc+binutils+glibc, **params)]

    limu_base = [builder('limu_base', initrd=1, builder=1, lib64=1, tools2=1, quick_boot=1, **params)]

    imagePackage = img

    kernel = linux
    boot = limu_base + busybox + unionfs + linux
    root = limu_base + busybox + make + kmod + linux + linuxhdr + link + binutils + gcc + glibc + zlib + squashfs

    #root = [builder('executable_stripper', packages=root, **params)]

    return (kernel, boot, root)

def buildFromX86_64(img, **params):
    global imagePackage
    imagePackage = img

    make = [builder('make', **params)]

    binutils = [builder('binutils', gold=0, doc=1, version='2.26', **params)]
    linuxhdr = [builder('linux', headers=1, **params)]
    gawk = [builder('gawk', **params)]
    glibc = [builder('glibc', linuxhdr+gawk, gold=0, **params)]
    gcc = [builder('gcc', bootstrap=0, gold=0, cpp=1, shared=1, libstdcxx=1, libquadmath=1, libsanitizer=1, pic=1, disable_multilib=1, **params)]

    busybox = [builder('busybox', version='1.26.2', **params)]
    kmod = [builder('kmod', **params)]

    m4 = [builder('m4', **params)]
    flex = [builder('flex', m4, **params)]
    bc = [builder('bc', flex, **params)]
    perl = [builder('perl', **params)]
    linux = [builder('linux', bc+perl, **params)]

    pkg_config = [builder('pkg_config', **params)]
    fuse = [builder('fuse', **params)]
    unionfs = [builder('unionfs_fuse', fuse + pkg_config, **params)]

    zlib = [builder('zlib', **params)]
    squashfs = [builder('squashfs', zlib, **params)]

    limu_base = [builder('limu_base', initrd=1, builder=1, lib64=1, tools2=1, quick_boot=1, **params)]

    kernel = linux
    boot = limu_base + busybox + unionfs + linux
    root = limu_base + busybox + make + kmod + linux + binutils + gcc + glibc + zlib + squashfs

    return (kernel, boot, root)

def buildImageFromX86_64(img, extras = [], **params):
    kernel, boot, root = buildFromX86_64(img, **params)

    img = builder('limu_image', [],
            kernel_package = ','.join(kernel),
            boot_packages = ','.join(boot),
            root_packages = ','.join(root + extras),
            **params)

    return [img]
        
def buildImageFromI386(img, extras = [], **params):
    kernel, boot, root = buildFromI386(img, **params)

    img = builder('limu_image', [],
            kernel_package = ','.join(kernel),
            boot_packages = ','.join(boot),
            root_packages = ','.join(root + extras),
            **params)

    return [img]

if __name__ == '__main__':
    print 'x86_64 %s' % ','.join(buildX86_64Image())
