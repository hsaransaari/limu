from executors import *
import builders, core
import sys, os, platform, multiprocessing

def PrepareParams(params):
    if params.get('host_tool', 0):
        params.setdefault('prefix', os.getcwd() + '/tools')

    params = GenericPrepareParams(params)

    params.setdefault('dest', os.getcwd() + '/work/dest')
    params.setdefault('arch', platform.machine())
    params.setdefault('num_threads', multiprocessing.cpu_count())
    params.setdefault('produce_package', 1)

    return params

def PrepareInstructions(params, instructions):
    instructions = GenericPrepareInstructions(params, instructions)
    out = []
    out.append(['executor', 'host', 0])
    if not params.get('produce_package', 1):
        out.append(['produce_package', 0])
    out.extend(instructions)
    out.append(['execute', 'touch %s/INSTALL_COMPLETED' % params['dest']])
    return out

def Execute(instructions):
    GenericExecute(instructions)

    produce_package = 1

    cwd = os.getcwd()

    core.shell.remove('work')
    core.shell.mkdir('work/build')

    core.shell.chdir('work/build')

    for i in instructions:
        if i[0] == 'extract':
            assert i[1][0] == 'hash'
            fn = core.cache.hashToFile(i[1][1])
            core.shell.shExec('tar xf %s' % fn)

        elif i[0] == 'produce_package':
            produce_package = int(i[1])

        elif i[0] == 'file':
            assert i[2][0] == 'hash'
            core.shell.shExec('cp %s %s' % (core.cache.hashToFile(i[2][1]), i[1]))

        elif i[0] == 'mkdir':
            core.shell.mkdir(i[1])

        elif i[0] == 'chdir':
            core.shell.chdir(i[1])

        elif i[0] == 'execute':
            core.shell.shExec(i[1])

        elif i[0] == 'prepend':
            core.shell.shExec("echo '%s' > tmp_file" % i[2])
            core.shell.shExec('cat %s >> tmp_file' % i[1])
            core.shell.shExec('mv tmp_file %s' % i[1])

        elif i[0] == 'append':
            f = open(i[1], 'a')
            f.write(i[2] + '\n')
            f.close()

        elif i[0] == 'copy':
            core.shell.shExec('cp "%s" "%s"' % (i[1], i[2]))

        elif i[0] == 'move':
            core.shell.shExec('mv "%s" "%s"' % (i[1], i[2]))

        else:
            raise RuntimeError('TODO: %s' % i[0])

    core.shell.chdir(cwd)

    #ret = False

    #if ret:
    #    core.shell.msg("building failed");
    #    sys.exit(1)

    if produce_package:
        return core.packageDirectory('work/dest')
