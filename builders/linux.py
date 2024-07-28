from core.builder import *

def Versions():
    return ['3.19']

def Build():
    if Ver()[0] == '3':
        Extract(URL('https://www.kernel.org/pub/linux/kernel/v3.x/linux-%s.tar.xz' % Ver()))
    else:
        Extract(URL('https://www.kernel.org/pub/linux/kernel/v4.x/linux-%s.tar.xz' % Ver()))

    Chdir('linux-%s' % Ver())
    #Make('mrproper')

    opts = ''

    if Option('target'):
        arch = Option('target').split('-')[0]
        if arch == 'i686': arch = 'x86'
        opts += ' ARCH=%s ' % arch

    if Option('cross_target'):
        opts += 'CROSS_COMPILE=%s- ' % Option('cross_target')

    if Option('config'):
        Mkdir('config_package')
        Chdir('config_package')
        for i in Option('config').split(','):
            Extract(Package(i))
        Chdir('..')
        Execute('cp config_package/kernel_config .config')

    if Option('menuconfig'):
        Make(opts + 'menuconfig')
        Mkdir(Dest())
        Copy('.config', Dest()+'/kernel_config')
        return

    if Option('allyesconfig'):
        Make('allyesconfig')

    if not Option('headers'):
        Make(opts + 'defconfig')
        File('limu_config', """
CONFIG_SQUASHFS=y
CONFIG_FUSE_FS=y
CONFIG_SMP=y
CONFIG_ATA_PIIX=n
CONFIG_VIRTIO=y
CONFIG_PNPACPI=y
CONFIG_BLK_DEV=y
CONFIG_BLK_DEV_LOOP=y
CONFIG_BLK_DEV_LOOP_MIN_COUNT=8
CONFIG_VIRTIO_PCI=y
CONFIG_VIRTIO_MMIO=y
CONFIG_VIRTIO_MMIO_CMDLINE_DEVICES=y
CONFIG_VIRTIO_BLK=y
CONFIG_CLKSRC_I8253=y
CONFIG_CLKEVT_I8253=y
CONFIG_I8253_LOCK=y
CONFIG_CLKBLD_I8253=y
""")
        Execute('cat limu_config >> .config')
        Make(opts + 'olddefconfig') # this is pretty new option, there is silentoldconfig but it doesn't work

        #else:
        #    #Append('limu_config', "CONFIG_MODULES=y")
        #    #Append('limu_config', "CONFIG_E1000=y")
        #    Execute('export KCONFIG_ALLCONFIG=limu_config')
        #    Make(opts + 'allmodconfig')

        if Option('fb', 0):
            Append('.config', "CONFIG_FB=y")
            Append('.config', "CONFIG_FB_BOOT_VESA_SUPPORT=y")
            Append('.config', "CONFIG_FB_VGA=y")
            Append('.config', "CONFIG_FB_VESA=y")
            Append('.config', "CONFIG_FB_SVGALIB=y")
            Append('.config', "CONFIG_FB_CIRRUS=y")
            Append('.config', "CONFIG_DRM_CIRRUS_QEMU=y")

        #Make(opts + 'dep')
        Make(opts)
        Make(opts + 'modules')
        Make(opts + 'modules_install INSTALL_MOD_PATH=%s' % Dest())
        Copy('arch/x86/boot/bzImage', Dest()+'/vmlinuz')
        Copy('System.map', Dest())
        Copy('.config', Dest()+'/kernel_config')

    Make(opts + 'headers_install INSTALL_HDR_PATH=%s/%s' % (Dest(), Prefix()))
