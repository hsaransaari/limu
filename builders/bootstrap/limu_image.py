from core.builder import *

def Versions():
    return ['0.1']

def Build():
    kernel_package = Option('kernel_package')
    boot_packages = Option('boot_packages')
    root_packages = Option('root_packages')

    Mkdir('iso')

    # Extract kernel

    Mkdir('kernel')
    Chdir('kernel')
    for i in kernel_package.split(','):
        Extract(Package(i))
    Chdir('..')

    Copy('kernel/vmlinuz', 'iso')

    # Extract root packages

    Mkdir('rootfs')
    Chdir('rootfs')
    for i in root_packages.split(','):
        Extract(Package(i))
    Chdir('..')

    # Prepare root fs

    Execute('mksquashfs rootfs iso/root.sqfs -no-duplicates -noI -noD -noF -noX -noappend > /dev/null')

    # Extract boot packages

    Mkdir('bootfs')
    Chdir('bootfs')

    Mkdir('lib')
    Move('../kernel/lib/modules', 'lib')

    for i in boot_packages.split(','):
        Extract(Package(i))

    Execute('find . > ../files.txt')
    Execute('find . | cpio --create --format=newc > ../initrd')
    Chdir('..')

    Execute('gzip initrd')
    Move('initrd.gz', 'iso/initrd')

    # Copy to dest

    Mkdir("%s/%s" % (Dest(), Prefix()))

    #Execute('grub-mkrescue -o limu.img iso')
    #Copy('limu.img', "%s/%s" % (Dest(), Prefix()))

    Move('files.txt', "%s/%s" % (Dest(), Prefix()))
    #Move('tmp', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
    Move('iso/root.sqfs', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
    Move('iso/initrd', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
    Move('iso/vmlinuz', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
