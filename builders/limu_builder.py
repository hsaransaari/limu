from core.builder import *

init_script_initrd = """
set -x
echo 'Limu builder initrd %s'
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
set -x
echo 'Preparing builder'
mount /dev/vda /mnt
mkfs.ext2 -q /dev/vdb
mount /dev/vdb /scratch
chown -R 1000:1000 /scratch
/usr/bin/setuidgid 1000:1000 /usr/bin/env -i RESOURCES=/mnt HOME=/scratch TERM="$TERM" PS1='\u:\w$ ' PATH=/bin:/usr/bin:/sbin:/usr/sbin:/tools/bin /mnt/user.sh || (echo 'build failed, starting debugging shell'; sh)
dd if=/mnt/scratch/package.tar.gz of=/dev/vdc
echo 'Expecting to boot soon'
echo b > /proc/sysrq-trigger
sh
"""

def Versions():
    return ['0.1']

def Build():
    initrd = int(Option('initrd', 0))
    builder = int(Option('builder', 0))
    tools_link = int(Option('tools_link', 0))

    Mkdir(Dest())
    Chdir(Dest())

    for i in ['dev', 'sys', 'proc', 'etc', 'var', 'tmp', 'root', 'mnt', 'usr', 'lib', 'bin', 'sbin', 'usr/bin', 'lib/modules']:
        Mkdir(i)

    if not initrd:
        Mkdir('boot/old_root')

    Append('etc/hostname', 'limu')
    Append('etc/passwd', 'root:x:0:0:root:/root:/bin/sh')
    Append('etc/group', 'root:x:0:')
    Append('etc/ld.so.conf', '/lib')
    Append('etc/ld.so.conf', '/usr/lib')

    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.1')
    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.2')
    Execute('ln -s ld-linux.so.2 lib/ld-lsb.so.3')
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
