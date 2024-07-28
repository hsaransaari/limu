from core.builder import *

boot_script = """#!/bin/bash
set -e -x

cp /root/user.sh /root/user.sh.2
rm /root/user.sh

mount /dev/sda /mnt
mkfs.ext2 -q -F /dev/sdb
mkdir /scratch
ln -s /mnt/tools /tools
mount /dev/sdb /scratch
useradd -s /bin/bash eemeli
chown eemeli:eemeli /scratch

sudo -u eemeli /mnt/user.sh

dd if=/scratch/package.tar.gz of=/dev/sdc
sync
echo 1 > /proc/sys/kernel/sysrq
echo b > /proc/sysrq-trigger
rm /root/.bashrc
"""

def Versions():
    return ['0.1']

def Build():
    v = Option('debian', '6.0.10')

    Fetch('image.iso', URL("http://cdimage.debian.org/mirror/cdimage/archive/%s-live/i386/iso-hybrid/debian-live-%s-i386-rescue.iso" % (v, v)))

    Execute('bsdtar -x -f image.iso -O live/vmlinuz > kernel')
    Execute('bsdtar -x -f image.iso -O live/initrd.img > initrd')

    Mkdir('extracted')
    Chdir('extracted')
    Execute('gzip -dc ../initrd | cpio -id')

    Append('scripts/init-bottom/ORDER', "echo '[ -e /root/user.sh ] && chmod +x /root/user.sh && /root/user.sh' >> ${rootmnt}/root/.bashrc")
    for line in boot_script.splitlines():
        Append('scripts/init-bottom/ORDER', "echo '%s' >> ${rootmnt}/root/user.sh" % line)
    Execute('rm scripts/live-bottom/24preseed')

    Execute('find . | cpio -H newc -o > ../initrd.new')
    Chdir('..')

    Mkdir("%s/%s/qemu_debian" % (Dest(), Prefix()))
    Move('initrd.new', "%s/%s/qemu_debian/initrd" % (Dest(), Prefix()))
    Move('kernel', "%s/%s/qemu_debian/kernel" % (Dest(), Prefix()))
