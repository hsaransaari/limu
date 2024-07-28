import os, sys

def msg(s, *a):
    print >> sys.stderr, '* %s' % (s % a)

def shExec(s, mayFail = False):
    msg('EXEC  %s', s)
    ret = os.system(s)
    if ret and not mayFail:
        msg("shell execute returned %d: %r", ret, s)
        raise RuntimeError('shExec failed')
    return ret

def rename(old, new):
    shExec('mv "%s" "%s"' % (old, new))

def remove(p):
    if os.path.exists(p):
        shExec('rm -fr "%s"' % p)

def mkdir(p):
    p = p.replace('//', '/')
    msg('MKDIR %s', p)
    if not os.path.exists(p):
        os.makedirs(p)

def chdir(p):
    msg('CHDIR %s', p)
    os.chdir(p)
