# This script builds a Limu builder image using Debian 6.0.10 live image

import core, os

# Versions

versions = { 
#    'gcc':           '4.9.4',
#    'lfs_gcc':       '4.9.4',
#    'lfs_libstdcxx': '4.9.4',
#    'binutils':      '2.25',
    'glibc':         '2.21',
#    'bison':         '3.0.4',
#    'flex':          '2.5.39',
#    'grub':          '2.00',
#    'linux':         '3.19',
#    'busybox':       '1.26.2',
}

# Helpers

def build(executor, builder_, **params):
    builder_ = 'bootstrap.' + builder_
    params.setdefault('version', versions.get(builder_, core.getLatestVersion(builder_)))
    print 'executor', executor, 'builder', builder_
    return core.execute(executor, builder_, params)

def hostTool(name, tools = [], **opts):
    return build('host', name, host_tool=1, host_tools=tools, **opts)

def lfsPackage(name, tools = [], **opts):
    return build('qemu_debian', name,
        cross='i686-lfs-linux-gnu',
        tools=tools,
        **opts)

def lfsBuilder(name, img, root = [], **opts):
    return build('qemu_builder', name,
        boot=img,
        cross='i686-lfs-linux-gnu',
        root=root,
        **opts)

def builder(name, img, root = [], **opts):
    return build('qemu_builder', name,
        boot=img,
        root=root,
        **opts)

def rebase(pkg, from_ = '/', to_ = '/'):
    return build('host', 'package_rebaser',
        package=pkg,
        src=from_,
        dst=to_)

def buildLFSFromDebian(**p):
    def debianTool(name, tools = [], **opts):
        opts.update(p)
        return build('qemu_debian', name,
            tool=1,
            lfs=1,
            target='i686-lfs-linux-gnu',
            tools=tools,
            **opts)

    # Add modified Debian live image as a host tool.

    p['host_tools'] += [hostTool('qemu_debian_images', [hostTool('libarchive')])]

    # Build some tools to build software for new image.

    binutils   = debianTool('lfs_binutils')
    gcc        = debianTool('lfs_gcc',       [binutils], step=1)
    linuxhdr   = debianTool('linux',         [], headers=1)
    glibc      = debianTool('lfs_glibc',     [binutils, gcc, linuxhdr])
    libstdcxx  = debianTool('lfs_libstdcxx', [binutils, gcc, linuxhdr, glibc])
    binutils2  = debianTool('lfs_binutils',  [binutils, gcc, linuxhdr, glibc, libstdcxx], step=2)
    gcc2       = debianTool('lfs_gcc',       [binutils, gcc, linuxhdr, glibc, libstdcxx, binutils2], step=2)
    make       = debianTool('make')

    compiler   = [binutils, gcc, linuxhdr, glibc, libstdcxx, binutils2, gcc2, make]

    # Make a simple builder image.

    #busybox = builder('busybox', img, compiler, build_host='i686-lfs-linux-gnu', **p)
    busybox = lfsPackage('busybox', compiler, **p)
    gawk = lfsPackage('gawk', compiler, **p)

    img = build('qemu_debian', 'lfs_image',
        kernel_package=lfsPackage('linux', [binutils, gcc], minimal=1, **p),
        packages= [ busybox, lfsPackage('lfs_base', [], initrd=1, builder=1, **p) ], **p)

    # Build system for temporary gcc and stuff.

    build_system = map(lambda x: rebase(x, '/tools', '/'), compiler) + [gawk]
    build_system += [busybox]
    build_system += [debianTool('lfs_base', [], builder=1)]

    tmp_build_system = []
    tmp_build_system += [rebase(linuxhdr, '/tools', '/usr')]
    tmp_build_system += [lfsBuilder('busybox', img, build_system + tmp_build_system, **p)]
    tmp_build_system += [lfsBuilder('binutils', img, build_system + tmp_build_system, gold=0, **p)]
    tmp_build_system += [lfsBuilder('glibc', img, build_system + tmp_build_system, **p)]
    tmp_build_system += [lfsBuilder('gcc', img, build_system + tmp_build_system, **p)]
    tmp_build_system += [lfsBuilder('make', img, build_system + tmp_build_system, **p)]

    linuxhdr2 = rebase(linuxhdr, '/tools', '/usr')

    build_system = map(lambda x: rebase(x, '/tools', '/'), [
            linuxhdr,
            debianTool('gawk'),
            debianTool('make'),
            debianTool('bash', compiler + [debianTool('bison')]),
            debianTool('busybox', [], no_prefix=0, version='1.23.2')
        ])
    build_system += tmp_build_system
    build_system += [debianTool('lfs_base', [], builder=1, tools_link=1)]
    #build_system += [builder('run_ldconfig', img, build_system)]
    return img, build_system

def buildI386Image(**p):
    img, build_system = buildLFSFromDebian(**p)

    # Now we should have a working build system. However, build compiling tools one
    # more time to get rid of oddities in bootstrapping.

    binutils = [builder('binutils', img, build_system, gold=0, **p)]
    gcc = [builder('gcc', img, build_system, **p)]
    glibc = [builder('glibc', img, build_system, **p)]
    make = [builder('make', img, build_system, **p)]
    gawk = [builder('gawk', img, build_system, **p)]
    linuxh = [builder('linux', img, build_system, headers=1, **p)]
    busybox = [builder('busybox', img, build_system, **p)]
    lfs_base = [builder('lfs_base', img, build_system, builder=1, **p)]

    # We could avoid this phase, but let's make sure that new tools are compiled
    # with themselves.

    tmp_base = lfs_base + binutils + gcc + glibc + make + linuxh + busybox

#    binutils = [builder('binutils', img, tmp_base, gold=0, **p)]
#    gcc = [builder('gcc', img, tmp_base, **p)]
#    glibc = [builder('glibc', img, tmp_base + gawk, **p)]
#    make = [builder('make', img, tmp_base, **p)]
#    gawk = [builder('gawk', img, tmp_base, **p)]
#    busybox = [builder('busybox', img, tmp_base, **p)]
#    lfs_base = [builder('lfs_base', img, tmp_base, builder=1, **p)]

    miniBase = lfs_base + busybox
    base = miniBase + glibc + binutils + gcc + make + linuxh

    # More tools, nothing critical anymore.

    bash = [builder('bash', img, base, default_sh=1, **p)]

    strace = [builder('strace', img, base, **p)]
    gawk = [builder('gawk', img, base, **p)]
    python = [builder('python', img, base, **p)]

    m4 = [builder('m4', img, base, **p)]
    perl = [builder('perl', img, base, **p)]
    coreutils = []#rebase(builder('coreutils', img, base + perl, **p), '/usr/', '/')]
    flex = [builder('flex', img, base + m4, **p)]
    bc = [builder('bc', img, base + flex, **p)]

    bison = [builder('bison', img, base + m4 + perl, **p)]
    grub = [builder('grub', img, base + m4 + bison + flex, **p)]

    ncurses = [builder('ncurses', img, base, **p)]
    vim = [builder('vim', img, base + ncurses, **p)]

    kmod = [builder('kmod', img, base, **p)]
    linux = [builder('linux', img, base + bash + bc + perl + kmod, minimal=1, **p)]

    groff = [builder('groff', img, base + perl, **p)]

    zlib = [builder('zlib', img, base, **p)]
    squashfs = [builder('squashfs', img, base + zlib, **p)]

    pkg_config = [builder('pkg_config', img, base, **p)]
    fuse = [builder('fuse', img, base, **p)]
    unionfs = [builder('unionfs_fuse', img, base + pkg_config + fuse, **p)]

    e2fsprogs = [builder('e2fsprogs', img, base, dev_libs=0, **p)]

    strace = [builder('strace', img, base, **p)]

    # Let's grab the limu source itself also.

    #limu_src = [builder('limu_src', img, miniBase, prefix='/')]

    limu_base = [builder('limu_base', img, miniBase, initrd=1, builder=1, **p)]

    packages = limu_base + busybox + glibc + binutils + gcc + make + linuxh + bash + ncurses + vim + python + squashfs + zlib + grub + bc + perl + groff + gawk + e2fsprogs + m4 + bison + flex + strace
#packages = builder('executable_stripper', img, base, packages=packages)

    img = builder('limu_image', img, miniBase + glibc + gcc + grub + squashfs + zlib,
            kernel_package = linux,
            boot_packages = limu_base + busybox + e2fsprogs + unionfs + linux,
            root_packages = packages, **p)

    return img

if __name__ == '__main__':
    print buildI386FromDebian()
