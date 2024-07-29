import sys
sys.dont_write_bytecode = 1
import chains, chains.qemu, chains.debian, chains.i386, chains.x86_64, chains.x11

def main(**p):
    p.setdefault('host_tools', chains.qemu.getHostQemu())

    # Deterministic computation ensures that results don't depend on the host.
    # This feature is however currently broken and it's also extremely slow as
    # everything is emulated.
    p.setdefault('deterministic', False)

    # Start building a system using Debian CD image.

    p['qemu_arch'] = 'i386'

    i386booted = chains.debian.buildI386Image(**p)

    p.setdefault('deterministic', True)
    i386builder = chains.i386.buildI386Image(i386booted, **p)
    #x = x11.buildX11Packages(i386img)

    # Let's jump from i386 to x86-64.

    x86_64booted = chains.x86_64.buildImageFromI386(i386builder, **p)

    p['qemu_arch'] = 'x86_64'

    x86_64builderX = chains.x86_64.buildImageFromX86_64(x86_64booted, **p)
    # NOTE: Second build fixes an issue, but shouldn't be needed.
    x86_64builder = chains.x86_64.buildImageFromX86_64(x86_64builderX, **p)

    # Let's get some software! 

    bash = [chains.x86_64.builder('bash', **p)]
    ncurses = [chains.x86_64.builder('ncurses', **p)]
    vim = [chains.x86_64.builder('vim', ncurses, **p)]
    screen = [chains.x86_64.builder('screen', ncurses, **p)]

    x11 = []
    x11 = chains.x11.buildX11Packages(x86_64builder, **p)
    python = [chains.x86_64.builder('python', x11, virtualenv=1, **p)]
    #python3 = [chains.x86_64.builder('python', x11, virtualenv=1, version='3.10.12', **p)]
    python3 = []
    x11 += python + python3
    #x11 += [chains.x86_64.builder('firefox', x11, **p)]
    x11 += [chains.x86_64.builder('wget', x11, **p)]
    x11 += [chains.x86_64.builder('fluxbox', x11, **p)]
    x11 += [chains.x86_64.builder('fltk', x11, **p)]
    x11 += [chains.x86_64.builder('dillo', x11, **p)]

    x11 += [chains.x86_64.builder('dhcpcd', x11, **p)]

    x11 += [chains.x86_64.builder('acpid', [], **p)]

    # This writes /user.sh, which starts Xorg and bash.
    start = [chains.x86_64.builder('limu_start', **p)]

    image = chains.x86_64.buildImageFromX86_64(x86_64builder, bash + ncurses + vim + screen + x11 + start, uid=0, gid=0, fb=1, allyesconfig=1, **p)

    print image


if __name__ == '__main__':
    main(**dict([i.split('=',1) for i in sys.argv[1:]]))
