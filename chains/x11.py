# This script builds a Limu builder using an existing Limu builder

import core, os, sys

# Versions

versions = {}

x11_src_pkg_data = """applewmproto-1.4.2 bdftopcf-1.0.3 bigreqsproto-1.1.2 compositeproto-0.4.2 damageproto-1.2.1
dmxproto-2.3.1 dri2proto-2.6 encodings-1.0.4 fixesproto-5.0 font-adobe-75dpi-1.0.3 font-adobe-100dpi-1.0.3
font-adobe-utopia-75dpi-1.0.4 font-adobe-utopia-100dpi-1.0.4 font-adobe-utopia-type1-1.0.4 font-alias-1.0.3
font-arabic-misc-1.0.3 font-bh-75dpi-1.0.3 font-bh-100dpi-1.0.3 font-bh-lucidatypewriter-75dpi-1.0.3
font-bh-lucidatypewriter-100dpi-1.0.3 font-bh-ttf-1.0.3 font-bh-type1-1.0.3 font-bitstream-75dpi-1.0.3
font-bitstream-100dpi-1.0.3 font-bitstream-type1-1.0.3 font-cronyx-cyrillic-1.0.3 font-cursor-misc-1.0.3
font-daewoo-misc-1.0.3 font-dec-misc-1.0.3 font-ibm-type1-1.0.3 font-isas-misc-1.0.3 font-jis-misc-1.0.3
font-micro-misc-1.0.3 font-misc-cyrillic-1.0.3 font-misc-ethiopic-1.0.3 font-misc-meltho-1.0.3 font-misc-misc-1.1.2
font-mutt-misc-1.0.3 font-schumacher-misc-1.1.2 font-screen-cyrillic-1.0.4 font-sony-misc-1.0.3 font-sun-misc-1.0.3
font-util-1.3.0 font-winitzki-cyrillic-1.0.3 font-xfree86-type1-1.0.4 fontsproto-2.1.2 glproto-1.4.15 iceauth-1.0.5
inputproto-2.2 kbproto-1.0.6 libAppleWM-1.4.1 libFS-1.0.4 libICE-1.0.8 libSM-1.2.1 libWindowsWM-1.0.1 libX11-1.5.0
libXScrnSaver-1.2.2 libXau-1.0.7 libXaw-1.0.11 libXcomposite-0.4.3 libXcursor-1.1.13 libXdamage-1.1.3 libXdmcp-1.1.1
libXext-1.3.1 libXfixes-5.0 libXfont-1.4.5 libXft-2.3.1 libXi-1.6.1 libXinerama-1.1.2 libXmu-1.1.1 libXpm-3.5.10
libXrandr-1.3.2 libXrender-0.9.7 libXres-1.0.6 libXt-1.1.3 libXtst-1.2.1 libXv-1.0.7 libXvMC-1.0.7 libXxf86dga-1.1.3
libXxf86vm-1.1.2 libdmx-1.1.2 libfontenc-1.1.1 libpciaccess-0.13.1 libpthread-stubs-0.3 libxcb-1.8.1 libxkbfile-1.0.8
luit-1.1.1 makedepend-1.0.4 mkfontdir-1.0.7 mkfontscale-1.1.0 randrproto-1.3.2 recordproto-1.14.2 renderproto-0.11.1
resourceproto-1.2.0 scrnsaverproto-1.2.2 sessreg-1.0.7 setxkbmap-1.3.0 smproxy-1.0.5 util-macros-1.17 videoproto-2.3.1
windowswmproto-1.0.4 x11perf-1.5.4 xauth-1.0.7 xbacklight-1.1.2 xbitmaps-1.1.1 xcb-proto-1.7.1 xcmiscproto-1.2.2
xcmsdb-1.0.4 xcursor-themes-1.0.3 xcursorgen-1.0.5 xdpyinfo-1.3.0 xdriinfo-1.0.4 xev-1.2.0 xextproto-7.2.1
xf86-input-evdev-2.7.0 xf86-input-joystick-1.6.1 xf86-input-keyboard-1.6.1 xf86-input-mouse-1.7.2
xf86-input-synaptics-1.6.1 xf86-input-vmmouse-12.8.0 xf86-input-void-1.4.0 xf86-video-ark-0.7.4 xf86-video-ast-0.93.10
xf86-video-ati-6.14.4 xf86-video-cirrus-1.4.0 xf86-video-dummy-0.3.5 xf86-video-fbdev-0.4.4 xf86-video-geode-2.11.13
xf86-video-glide-1.2.0 xf86-video-glint-1.2.7 xf86-video-i128-1.3.5 xf86-video-intel-2.19.0 xf86-video-mach64-6.9.1
xf86-video-mga-1.5.0 xf86-video-neomagic-1.2.6 xf86-video-newport-0.2.4 xf86-video-nv-2.1.18
xf86-video-openchrome-0.2.906 xf86-video-r128-6.8.2 xf86-video-savage-2.3.4 xf86-video-siliconmotion-1.7.6
xf86-video-sis-0.10.4 xf86-video-suncg6-1.1.1 xf86-video-sunffb-1.2.1 xf86-video-tdfx-1.4.4 xf86-video-tga-1.2.1
xf86-video-trident-1.3.5 xf86-video-v4l-0.2.0 xf86-video-vesa-2.4.0 xf86-video-vmware-12.0.2 xf86-video-voodoo-1.2.4
xf86-video-wsfb-0.4.0 xf86bigfontproto-1.2.0 xf86dgaproto-2.1 xf86driproto-2.1.1 xf86vidmodeproto-2.3.1 xgamma-1.0.5
xhost-1.0.5 xineramaproto-1.2.1 xinput-1.6.0 xkbcomp-1.2.4 xkbevd-1.1.3 xkbutils-1.0.3 xkeyboard-config-2.6 xkill-1.0.3
xlsatoms-1.1.1 xlsclients-1.1.2 xmodmap-1.0.7 xorg-docs-1.7 xorg-server-1.12.2 xorg-sgml-doctools-1.11 xpr-1.0.4
xprop-1.2.1 xproto-7.0.23 xrandr-1.3.5 xrdb-1.0.9 xrefresh-1.0.4 xset-1.2.2 xsetroot-1.1.0 xtrans-1.2.7 xvinfo-1.1.1
xwd-1.0.5 xwininfo-1.1.2 xwud-1.0.4
"""

x11_versions = dict([p.rsplit('-', 1) for p in x11_src_pkg_data.split()])
x11_packages = [p.rsplit('-', 1)[0] for p in x11_src_pkg_data.split()]

# Helpers

def build(executor, builder_, **params):
    params.setdefault('version', versions.get(builder_, core.getLatestVersion(builder_)))
    print 'executor', executor, 'builder', builder_
    return core.execute(executor, builder_, params)

def builder(name, root = [], **opts):
    return build('qemu_builder', name,
        boot=imagePackage,
        root=root,
        **opts)

def x11Builder(name, root = [], **opts):
    opts['pkg'] = "%s-%s" % (name, x11_versions[name])
    return builder('xorg', root, **opts)

def buildX11Packages(img, **p):
    global imagePackage
    imagePackage = img

    def b(name, deps = [], **p2):
        p2.update(p)
        return [builder(name, deps, **p2)]

    def x(name, deps = [], **p2):
        p2.update(p)
        return [x11Builder(name, deps, **p2)]

    gettext = b('gettext')
    perl = b('perl')
    expat = b('expat')
    xmlparser = b('cpan', perl + expat, author='MSERGEANT', pkg='XML-Parser-2.36')
    intltool = b('intltool', perl + xmlparser + expat)
    python = b('python')
    file = b('file')

    openssl = b('openssl', perl)
    m4 = b('m4', perl)
    autoconf = b('autoconf', perl+m4)

    clang = b('clang', b('python')+b('cmake')+b('groff', perl), modules="", version='3.6.2', shared=1, num_threads=2)
    pixman = b('pixman')
    libxml2 = b('libxml2')
    libxslt = b('libxslt', libxml2)

    libpciaccess = x('libpciaccess')
    pkg_config = b('pkg_config')
    libdrm = b('libdrm', libpciaccess + pkg_config)

    freetype = b('freetype')

    xproto = x('xproto')
    xextproto = x('xextproto')
    xtrans = x('xtrans')

    libxau = x('libXau', xproto + pkg_config)

    libpthread_stubs = x('libpthread-stubs')

    protos = []
    protos += x('kbproto')
    protos += x('inputproto')
    protos += x('glproto')
    protos += x('dri2proto')
    protos += x('xcmiscproto')
    protos += x('bigreqsproto')
    protos += x('randrproto')
    protos += x('renderproto')
    protos += x('fontsproto')
    protos += x('videoproto')
    protos += x('compositeproto')
    protos += x('recordproto')
    protos += x('scrnsaverproto')
    protos += x('resourceproto')
    protos += x('xineramaproto')
    protos += x('damageproto')
    protos += x('xcb-proto', python)
    protos += x('fixesproto')
    protos += x('xf86driproto')
    protos += x('xf86dgaproto')

    protos = b('package_combiner', packages=protos)

    x11 = []

    x11 += xproto + xextproto + xtrans + protos + libxau + libpthread_stubs + libpciaccess + libdrm + pixman + freetype
    x11 += pkg_config + perl + m4 + autoconf + openssl + file

    x11 += x('libxcb', libxslt + python + pkg_config + protos + libxau + libpthread_stubs + xproto) #, x11 + libxslt + python)
    x11 += x('libX11', x11)
    x11 += x('libXext', x11)
    x11 += x('libXfixes', x11)
    x11 += x('libXdamage', x11)

    fonts = []
    x11 += x('libfontenc', x11)
    x11 += x('libXfont', x11)
    x11 += x('mkfontdir', x11)
    x11 += x('mkfontscale', x11)
    x11 += x('bdftopcf', x11)
    x11 += x('font-util', x11)
    for f in x11_packages:
        if f.startswith('font-') and f != 'font-util':
            fonts += x(f, x11)

    mesa = b('mesa', x11 + pkg_config + clang + expat + python)
    x11 += mesa

    x11 += x('libxkbfile', x11)
    x11 += x('xorg-server', x11)# + b('gawk') + b('bash'))
    x11 += x('libXxf86dga', x11)
    x11 += x('libICE', x11)
    x11 += x('libSM', x11)
    x11 += x('libXt', x11)
    x11 += x('libXmu', x11)
    x11 += x('libXpm', x11 + b('gettext'))
    x11 += x('libXaw', x11)
    x11 += x('xkbcomp', x11)

    x11_apps = []
    x11_apps += x('xwininfo', x11)
    x11_apps += x('xkeyboard-config', x11 + gettext + perl + expat + xmlparser + intltool)
    x11_apps += b('xterm', x11 + b('ncurses'))
    x11_apps += b('tmux', b('libevent')+b('ncurses')) + b('libevent')

    x11_drivers = []
    x11_drivers += x('xf86-input-keyboard', x11)
    x11_drivers += x('xf86-input-mouse', x11)
#    x11_drivers += x('xf86-video-cirrus', x11)
    x11_drivers += x('xf86-video-vesa', x11)
    #x11_drivers += x('xf86-video-vga', x11)
    x11_drivers += x('xf86-video-fbdev', x11)
#    x11_drivers += x('xf86-video-dummy', x11)

    return x11 + x11_drivers + fonts + x11_apps
