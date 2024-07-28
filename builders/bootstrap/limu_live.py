from core.builder import *

def Versions():
    return ['0.1']

def Build():
    kernel_package = Option('kernel_package')
    packages = Option('packages')

    # Extract kernel

    Mkdir('kernel')
    Chdir('kernel')
    for i in kernel_package.split(','):
        Extract(Package(i))
    Chdir('..')

    # Extract packages

    Mkdir('rootfs')
    Chdir('rootfs')
    if packages:
        print packages
        for i in packages.split(','):
            Extract(Package(i))

    # Prepare

    Mkdir('lib')
    Move('../kernel/lib/modules', 'lib')

    Execute('find . > ../files.txt')
    Execute('find . | cpio --create --format=newc > ../initrd')
    Chdir('..')
    Execute('gzip initrd')
    Move('initrd.gz', 'initrd')

    Mkdir('iso')
    Copy('kernel/vmlinuz', 'iso')
    Copy('initrd', 'iso/initrd')

    Mkdir("%s/%s" % (Dest(), Prefix()))

    #Execute('grub-mkrescue -o limu.img iso')
    #Copy('limu.img', "%s/%s" % (Dest(), Prefix()))

    Move('files.txt', "%s/%s" % (Dest(), Prefix()))
    #Move('tmp', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
    Move('iso/initrd', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))
    Move('iso/vmlinuz', ("%s/%s" % (Dest(), Prefix())).replace('//', '/'))

