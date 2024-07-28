import sys
sys.dont_write_bytecode = True

import os, glob, tarfile, importlib
import executors
import core.cache, core.builder

def getBuilder(name):
    return importlib.import_module('builders.' + name)

def getExecutor(name):
    return importlib.import_module('executors.' + name)

def getLatestVersion(builderName):
    return getBuilder(builderName).Versions()[-1]

def getAllBuilders():
    return sorted([i for i in [i.split('/')[-1][:-3] for i in glob.glob('builders/*.py')] if i != '__init__'])

def execute(executorName, builderName, params):
    # Join lists with comma in input parameters.

    for k, v in params.items():
        if type(params[k]) == list:
            params[k] = ','.join(v)

    params = getExecutor(executorName).PrepareParams(params)

    builder.Clear()
    builder._builder = builderName
    builder._params.update(params)
    getBuilder(builderName).Build()

    instructions = builder._instructions
    instructions = getExecutor(executorName).PrepareInstructions(params, instructions)
    instructions = collectDatas(instructions)

    h = core.cache.hashInstructions(instructions)
    if params.get('execution_cache', 1):
        c = cache.find(h)
        if c:
            print "EXECUTE_CACHE_HIT %s %s %s => %s" % (executorName, builderName, h, c)
            return c[1]
        else:
            print "EXECUTE_CACHE_MISS %s %s %s" % (executorName, builderName, h)
    sys.stdout.flush()

    pkg = executeInstructions(instructions)
    if pkg:
        open('execution.log', 'a').write("%s %s %s\n" % (h, pkg, repr(instructions)))
        cache.cacheExecution(instructions, pkg)
        return cache.find(h)[1]

def executeInstructions(instructions):
    if instructions[0][0] == 'executor':
        return getExecutor(instructions[0][1]).Execute(instructions[1:])
    else:
        raise RuntimeError('expecting executor as first instruction')

def collectData(d):
    if d[0] == 'url':
        return core.cache.fetchURL(d[1], d[2])
    if d[0] == 'file':
        return core.cache.fetchLocalFile(d[1], d[2])
    return d

def collectDatas(instructions):
    out = []
    for ins in instructions:
        if ins[0] == 'provides':
            continue
        elif ins[0] == 'extract':
            ext = ins[2]
            if not ext:
                if ins[1][1].endswith('.tar.gz'):
                    ext = 'tar.gz'
                elif ins[1][1].endswith('.tar.bz2'):
                    ext = 'tar.bz2'
                elif ins[1][1].endswith('.tar.xz'):
                    ext = 'tar.xz'
                else:
                    ext = 'tar.gz'
                    #raise RuntimeError('cannot extract: %s' % ext)

            out.append(['extract', collectData(ins[1]), ext])
        elif ins[0] == 'fetch':
            out.append(['file', ins[1], collectData(ins[2])])
        elif ins[0] == 'file':
            out.append(['file', ins[1], core.cache.hashResource(ins[2])])
        else:
            out.append(ins)
    return out

def findFiles(p, rp):
    ret = []
    for fn in os.listdir(p):
        a = p + '/' + fn
        ret += [rp + '/' + fn]
        if os.path.isdir(a):
            ret += findFiles(a, rp + '/' + fn)
    return ret

def packageDirectory(path): 
    shell.mkdir('work')

    if not os.path.exists("%s/INSTALL_COMPLETED" % path):
        print('DEBUG', path)
        raise RuntimeError('attempting to build incomplete package')
    shell.remove("%s/INSTALL_COMPLETED" % path)

    shell.shExec('./bin/lpack --verbose --create --source %s --destination work/package.tar.gz' % path)

    h2 = cache.hashFile('work/package.tar.gz', False)

    shell.mkdir('packages')
    pkgFile = 'packages/%s.tar.gz' % h2
    shell.shExec('mv work/package.tar.gz %s' % pkgFile)

    h3 = cache.hashFile(pkgFile, True)
    assert h2 == h3
    return h2

def makeHostTools(pkgs):
    dst = 'tools'

    shell.remove(dst)
    shell.mkdir(dst)

    p = './' + os.getcwd().strip('/') + '/' + dst
    n = len(p.split('/'))-1

    for pkg in pkgs:
        shell.remove("tools.tmp")
        shell.mkdir("tools.tmp")
        shell.shExec('tar -C tools.tmp -xof %s %s' % (cache.hashToFile(pkg), p))
        shell.shExec('cp -r tools.tmp/%s/* %s' % (p, dst))
        shell.remove("tools.tmp")

def makeSquashFS(p):
    shell.shExec('mksquashfs %s image.sqfs -no-duplicates -noI -noD -noF -noX -noappend > /dev/null' % p)
    return "image.sqfs"
