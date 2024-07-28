from core.builder import *

init_script_initrd = """
echo 'Limu initrd %s'
mount -t devtmpfs devtmpfs /dev 
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t tmpfs tmpfs /tmp
"""

init_script_nonbuilder = """
ln -sv /proc/self/mounts /etc/mtab
echo 'Welcome.'
sh
"""

init_script_builder = """
echo 'Preparing builder'
mount /dev/vda /mnt
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys
mount --bind /tmp /mnt/tmp
echo "Some random string to seed random" > /dev/random
init_random
mkfs.ext2 -q /dev/vdb
mount /dev/vdb /mnt/scratch
chown -R 1000:1000 /mnt/scratch
chroot /mnt setuidgid 1000:1000 /usr/bin/env -i RESOURCES=/ HOME=/scratch TERM="$TERM" PS1='\u:\w$ ' PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin /user.sh || (echo 'build failed, starting debugging shell'; sh)
dd if=/mnt/scratch/package.tar.gz of=/dev/vdc
echo 'Expecting to boot soon'
echo b > /proc/sysrq-trigger
sh
"""

init_random_src = """
#include <unistd.h>
#include <linux/random.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
    int fd = open("/dev/random", O_RDWR);
    int val = 65535;
    ioctl(fd, RNDADDTOENTCNT, &val);
    fd = open("/dev/urandom", O_RDWR);
    ioctl(fd, RNDADDTOENTCNT, &val);
    return 0;
}
"""

def Versions():
    return ['0.1']

def Build():
    initrd = int(Option('initrd', 0))
    builder = int(Option('builder', 0))
    tools_link = int(Option('tools_link', 0))

    File('init_random.c', init_random_src)
    Execute('cc -static -o init_random init_random.c')
    Mkdir('%s/bin' % (Dest()))
    Execute('cp init_random %s/bin' % (Dest()))

    Mkdir(Dest())
    Chdir(Dest())

    for i in ['dev', 'sys', 'proc', 'etc', 'var', 'tmp', 'root', 'mnt', 'usr', 'lib', 'bin', 'sbin', 'usr/bin', 'lib/modules']:
        Mkdir(i)

    if not initrd:
        Mkdir('boot/old_root')

    Append('etc/hostname', 'lfslimu')
    Append('etc/passwd', 'root:x:0:0:root:/root:/bin/sh')
    Append('etc/group', 'root:x:0:')
    Append('etc/ld.so.conf', '/lib')
    Append('etc/ld.so.conf', '/usr/lib')

    #Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.1')
    #Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.2')
    #Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.3')
    Execute('ln -s gcc usr/bin/cc')

    if tools_link:
        Execute('ln -s . tools')

    if builder:
        Append('etc/passwd', 'eemeli:x:1000:1000:eemeli:/scratch:/bin/sh')
        Append('etc/group', 'eemeli:x:1000:')
        Mkdir('scratch')
        Mkdir('home/eemeli')

    if initrd:
        s = '#!/bin/sh\n'
        s += init_script_initrd % Ver()
        if builder:
            s += init_script_builder
        else:
            s += init_script_nonbuilder

        File('init', s)
        Execute('chmod +x init')
