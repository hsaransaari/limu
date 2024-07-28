#!/bin/bash

# You need to extract tar package to limu root given by
#   python2 desktop.py

set -e -x

dd if=/dev/zero of=scratch.raw bs=1M count=512

#qemu-system-i386 \

./tools/bin/qemu-system-x86_64 \
  -L tools/share/qemu/ \
  -machine type=pc,accel=kvm:xnu:tcg \
  -m 2048 \
  -net nic -net user \
  -rtc clock=vm \
  -no-reboot \
  -no-hpet \
  -serial stdio \
  -vga std \
  -drive file=usr/root.sqfs,format=raw,cache=none,if=virtio \
  -drive file=scratch.raw,format=raw,cache=none,if=virtio \
  -kernel usr/vmlinuz \
  -initrd usr/initrd \
  -append "root=/dev/ram0 loglevel=7 builder=0 video=vesafb fb=1 vga=0x343 console=ttyS0,38400n8 "

  #-net user,hostfwd=tcp::10022-:22 \
  #-netdev user,id=n1 -device virtio-net-pci,netdev=n1 \
  #-netdev user,id=mynet0,net=192.168.76.0/24,dhcpstart=192.168.76.9 \

  #-hda usr/root.sqfs \
#-display none \
#-nographic \
