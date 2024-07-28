from core.builder import *

init_script_initrd = """
set -x
echo 'Limu initrd %s'
mount -t devtmpfs devtmpfs /dev 
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts
mount -t proc proc /proc
mount -t sysfs sysfs /sys
mount -t tmpfs tmpfs /tmp
"""

init_script_builder = """
set -x
echo 'Preparing limu builder'

cat $0 > /dev/urandom
cat $0 > /dev/random

hostname limu

mount /dev/vda /mnt

PATH=$PATH:/usr/sbin

%(mkfs)s

mount /dev/vdb /mnt2
mkdir /mnt2/scratch
chown -R 1000:1000 /mnt2

unionfs -s -o cow,allow_other,dev,nosuid,uid=1000,gid=1000,nonempty /mnt=RO:/mnt2=RW /mnt3
mount --bind /dev /mnt3/dev
mount --bind /proc /mnt3/proc

chroot /mnt3 /usr/bin/setuidgid 1000:1000 /usr/bin/env -i RESOURCES=/ HOME=/scratch TERM="$TERM" PS1='\u:\w$ ' PATH=/bin:/usr/bin:/sbin:/usr/sbin%(path)s /user.sh || (echo 'build failed, starting debugging shell'; sh)

dd if=/mnt3/scratch/package.tar.gz of=/dev/vdc

echo 'Expecting to boot soon'
echo b > /proc/sysrq-trigger
sh
"""

def Versions():
    return ['0.1']

def Build():
    initrd = int(Option('initrd', 0))

    Mkdir(Dest())
    Chdir(Dest())

    for i in 'dev sys proc etc var tmp root mnt mnt2 mnt3 usr lib bin sbin usr/bin lib/modules'.split():
        Mkdir(i)

    if not initrd:
        Mkdir('boot/old_root')

    Append('etc/hostname', 'limu')
    Append('etc/hosts', '127.0.0.1  localhost loopback limu')
    Append('etc/hosts', '::1        localhost limu')

    Append('etc/passwd', 'root:x:0:0:root:/root:/bin/sh')
    Append('etc/group', 'root:x:0:')
    Append('etc/ld.so.conf', '/lib')
    Append('etc/ld.so.conf', '/usr/lib')

    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.1')
    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.2')
    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.3')
    Execute('ln -s gcc usr/bin/cc')
    if Option('link_lib64', 1):
        Execute('ln -s lib usr/lib64')

    Append('etc/passwd', 'eemeli:x:1000:1000:eemeli:/scratch:/bin/sh')
    Append('etc/group', 'eemeli:x:1000:')

    Append('sbin/quick_boot', 'echo b > /proc/sysrq-trigger')
    Execute('chmod +x sbin/quick_boot')

    Mkdir('scratch')
    Mkdir('home/eemeli')

    d = {}
    d['path'] = ':/tools/bin'

    if Option('tools2'):
        d['path'] += ':/tools2/bin'

    if Option('ext4'):
        d['mkfs'] = 'mkfs.ext4 -q -E lazy_itable_init -O sparse_super -m 0 /dev/vdb'
    else:
        d['mkfs'] = 'mkfs.ext2 -q -m 0 /dev/vdb'

    if initrd:
        s = '#!/bin/sh\n'
        s += init_script_initrd % Ver()
        s += init_script_builder % d

        File('init', s)
        Execute('chmod +x init')
