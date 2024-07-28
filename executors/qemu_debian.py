from executors import *
from core.instructions import URL
import builders, core
import sys, os, platform, multiprocessing

def PrepareParams(params):
    params = GenericPrepareParams(params)

    if 'tool' in params and int(params['tool']):
        params['prefix'] = '/tools'

    params['dest'] = '/scratch/dest'
    params['arch'] = 'i386'
    params['num_threads'] = 1
    params.setdefault('deterministic', False)
    if params['deterministic']:
        params.setdefault('rtc', '2014-04-14T22:30:00')
    params.setdefault('debian', '6.0.10')

    return params

def PrepareInstructions(params, instructions):
    instructions = GenericPrepareInstructions(params, instructions)

    out = []
    out.append(['executor', 'qemu_debian', 0])
    v = params['debian']
    out.append(['fetch', 'image.iso', URL("http://cdimage.debian.org/mirror/cdimage/archive/%s-live/i386/iso-hybrid/debian-live-%s-i386-rescue.iso" % (v, v))])
    if params.get('rtc', None):
        out.append(['rtc', params['rtc']])
    if params.get('tools', None):
        for t in params['tools'].split(','):
            out.append(['tool', ('hash', t)])
    out.extend(instructions)
    out.append(['execute', 'touch %s/INSTALL_COMPLETED' % params['dest']])
    return out

def Execute(instructions):
    GenericExecute(instructions)

    core.shell.remove('work')
    core.shell.mkdir('work/image')

    # Copy tools.

    anyTools    = False
    debianImage = None
    rtc         = None

    instructions2 = []

    for ins in instructions:
        if ins[0] == 'tool':
            if not anyTools:
                anyTools = True
                core.shell.mkdir('work/image/tools')
            assert ins[1][0] == 'hash'
            core.shell.shExec('tar xfo %s --strip-components 2 -C work/image/tools ./tools' % (core.cache.hashToFile(ins[1][1])))
        elif ins[0] == 'file' and ins[1] == 'image.iso':
            if not debianImage:
                debianImage = core.cache.hashToFile(ins[2][1])
            else:
                instructions2.append(ins)
        elif ins[0] == 'rtc':
            rtc = ins[1]
        else:
            instructions2.append(ins)

    instructions = instructions2

    f = open('work/image/user.sh', 'w')
    f.write("""#!/bin/bash
set -e -x
umask 022
export LC_ALL=POSIX
""")

    if anyTools:
        print >> f, 'export PATH=/tools/bin:/tools/sbin:$PATH'
    print >> f, 'cd /scratch'
    for s in instructions:
        if s[0] == 'extract':
            assert s[1][0] == 'hash'
            fn = "%s.%s" % (s[1][1], s[2])
            core.shell.shExec('cp %s work/image/%s' % (core.cache.hashToFile(s[1][1]), fn))
            print >> f, 'tar xf /mnt/%s' % fn
        elif s[0] == 'file':
            assert s[2][0] == 'hash'
            fn = s[2]
            core.shell.shExec('cp %s work/image/%s' % (core.cache.hashToFile(s[2][1]), s[2][1]))
            print >> f, 'cp /mnt/%s %s' % (s[2][1], s[1])
        elif s[0] == 'env':
            print >> f, 'export %s="%s"' % (s[1], s[2])
        elif s[0] == 'chdir':
            print >> f, 'cd %s' % s[1]
        elif s[0] == 'mkdir':
            print >> f, 'mkdir -p %s' % s[1]
        elif s[0] == 'execute':
            print >> f, '%s' % s[1]
        elif s[0] == 'prepend':
            assert not "'" in s[2]
            print >> f, "echo '%s' > tmp_file" % s[2]
            print >> f, 'cat %s >> tmp_file' % s[1]
            print >> f, 'mv tmp_file %s' % s[1]
        elif s[0] == 'append':
            assert not "'" in s[2]
            print >> f, "echo '%s' >> %s" % (s[2], s[1])
        elif s[0] == 'copy':
            print >> f, 'cp "%s" "%s"' % (s[1], s[2])
        elif s[0] == 'move':
            print >> f, 'mv "%s" "%s"' % (s[1], s[2])
        else:
            raise RuntimeError("bad cmd %r" % (s,))
    print >> f, 'tar cvf /scratch/package.tar -C /scratch/dest .'
    print >> f, 'gzip --fast -n /scratch/package.tar'
    f.close()

    core.shell.shExec('chmod +x work/image/user.sh')

    img = core.makeSquashFS('work/image')
    core.shell.shExec('mv %s work/image.sqfs' % img)
    img = 'work/image.sqfs'

    core.shell.shExec('qemu-img create -q -f qcow2 work/scratch.img  8G')
    core.shell.shExec('qemu-img create -q -f raw   work/result.img   512M')

    rtc_line = "-rtc base=%s,clock=vm " % rtc if rtc else " "

#-cpu host \
    core.shell.shExec('qemu-system-i386 \
-L tools/share/qemu \
-machine type=pc,accel=kvm:xen:tcg \
-m 3072 \
%s \
-net none \
-no-reboot \
-no-hpet \
-nographic \
-display none \
-hda %s \
-hdb work/scratch.img \
-cdrom %s \
-hdd work/result.img \
-kernel tools/qemu_debian/kernel \
-initrd tools/qemu_debian/initrd \
-append "1 console=ttyS0,38400n8 loglevel=8 fb=false boot=live netcfg/disable_dhcp=true"' % (rtc_line, img, debianImage))

    core.shell.mkdir('work/dest')
    core.shell.shExec('tar xfmo work/result.img -C work/dest')

    return core.packageDirectory('work/dest')
