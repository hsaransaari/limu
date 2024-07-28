from executors import *
import builders, core
import sys, os, platform, multiprocessing, tarfile

def PrepareParams(params):
    params = GenericPrepareParams(params)

    if 'tool' in params and int(params['tool']):
        params['prefix'] = '/tools'
    #else:
    #    params['prefix'] = '/usr'

    params['dest'] = '/scratch/dest'
    params.setdefault('qemu_arch', 'i386')
    params.setdefault('deterministic', False)
    if params['deterministic']:
        params.setdefault('rtc', '2024-04-14T22:30:00')
        params.setdefault('num_threads', 1)
    else:
        params.setdefault('num_threads', multiprocessing.cpu_count())

    return params

def PrepareInstructions(params, instructions):
    instructions = GenericPrepareInstructions(params, instructions)

    out = []
    out.append(['executor', 'qemu_builder', 0])
    out.append(['arch', params['qemu_arch']])
    out.append(['deterministic', params['deterministic']])
    if 'rtc' in params:
        out.append(['rtc', params['rtc']])
    out.append(['boot', ('hash', params['boot'])])
    if params['root']:
        for t in params['root'].split(','):
            out.append(['root', ('hash', t)])
    out.extend(instructions)
    out.append(['execute', 'touch %s/INSTALL_COMPLETED' % params['dest']])
    return out

def Execute(instructions):
    GenericExecute(instructions)

    core.shell.remove('work')
    core.shell.mkdir('work/boot')

    # Copy tools.

    image         = None
    rtc           = None
    arch          = None
    deterministic = False

    instructions2 = []

    for ins in instructions:
        if ins[0] == 'root':
            assert ins[1][0] == 'hash'
            core.shell.mkdir('work/image')
            #core.shell.shExec('tar xfoh %s --strip-components 1 -C work/image ./' % (core.cache.hashToFile(ins[1][1])))
            #core.shell.shExec('tar xfo %s --strip-components 1 -C work/image' % (core.cache.hashToFile(ins[1][1])))
            core.shell.shExec('./bin/lpack --extract --verbose --source %s --destination work/image' % (core.cache.hashToFile(ins[1][1])))
        elif ins[0] == 'boot':
            assert ins[1][0] == 'hash'
            #tar = tarfile.open(core.cache.hashToFile(ins[1][1]), 'r')
            #tar.extractall('work/boot')
            #tar.close()
            core.shell.shExec('tar xfo %s -C work/boot' % (core.cache.hashToFile(ins[1][1])))
            if os.path.exists('work/boot/usr/root.sqfs'):
                core.shell.shExec('unsquashfs -d work/image work/boot/usr/root.sqfs')
        elif ins[0] == 'rtc':
            rtc = ins[1]
        elif ins[0] == 'arch':
            arch = ins[1]
        elif ins[0] == 'deterministic':
            deterministic = ins[1]
        else:
            instructions2.append(ins)

    instructions = instructions2

    f = open('work/image/user.sh', 'w')
    f.write("""#!/bin/sh
set -e -x
umask 022
export LC_ALL=POSIX
export PATH=$PATH:/usr/bin
export PATH
""")

    print >> f, 'cd /scratch'
    for s in instructions:
        if s[0] == 'extract':
            assert s[1][0] == 'hash'
            fn = "%s.%s" % (s[1][1], s[2])
            core.shell.shExec('cp %s work/image/%s' % (core.cache.hashToFile(s[1][1]), fn))
            print >> f, 'tar xf $RESOURCES/%s' % fn
        elif s[0] == 'file':
            assert s[2][0] == 'hash'
            fn = s[2]
            core.shell.shExec('cp %s work/image/%s' % (core.cache.hashToFile(s[2][1]), s[2][1]))
            print >> f, 'cp $RESOURCES/%s %s' % (s[2][1], s[1])
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

    core.shell.shExec('mksquashfs work/image work/root.sqfs -no-duplicates -noI -noD -noF -noX > /dev/null')
    #core.shell.shExec('mksquashfs work/image work/boot/root.sqfs > /dev/null')
    img = 'work/root.sqfs'

    core.shell.shExec('qemu-img create -q -f qcow2 work/scratch.img   16G')
    core.shell.shExec('qemu-img create -q -f raw   work/result.img  1024M')

    if deterministic:
        accel = 'tcg'
        icount = '-icount shift=8,sleep=on'
    else:
        accel = 'kvm'
        icount = '-cpu host -smp 4'

    rtc_line = "-rtc base=%s,clock=vm " % rtc if rtc else " "

    core.shell.shExec('qemu-system-%s \
-L tools/share/qemu \
-machine type=pc,accel=%s \
-m 3072 \
%s \
%s \
-net none \
-no-reboot \
-no-hpet \
-display none \
-serial stdio \
-drive file=%s,format=raw,cache=none,if=virtio \
-drive file=work/scratch.img,format=qcow2,cache=none,if=virtio \
-drive file=work/result.img,format=raw,cache=none,if=virtio \
-kernel work/boot/usr/vmlinuz \
-initrd work/boot/usr/initrd \
-append "1 console=ttyS0,38400n8 loglevel=8 fb=false boot=live netcfg/disable_dhcp=true"' % (arch, accel, rtc_line, icount, img))

#-nographic \
#-net user,hostfwd=tcp::10022-:22 \

    core.shell.mkdir('work/dest')
    core.shell.shExec('tar xfmo work/result.img -C work/dest')

    return core.packageDirectory('work/dest')
