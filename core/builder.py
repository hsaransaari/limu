from core.instructions import *

def Clear():
    global _builder, _params, _instructions
    _builder      = None
    _params       = {}
    _instructions = []

def Builder():
    return _builder.split('.')[-1]
def Ver():
    return _params['version']
def Prefix():
    return _params['prefix']
def Dest():
    return _params['dest']
def Option(name, d = None):
    return _params.get(name, d)

def Provides(prog):
    _instructions.append(['provides', prog])
def Extract(pkg):
    _instructions.append(['extract', pkg, None])
def Fetch(name, pkg):
    _instructions.append(['fetch', name, pkg])
def File(fn, data):
    _instructions.append(['file', fn, data])
def Mkdir(p):
    _instructions.append(['mkdir', p])
def Chdir(p):
    _instructions.append(['chdir', p])
def Execute(cmd):
    _instructions.append(['execute', cmd])
def Make(cmd = ''):
    if 'install' in cmd.split():
        cmd = 'make ' + cmd
    else:
        cmd = 'make -j%d %s' % (_params['num_threads'], cmd)
    _instructions.append(['execute', cmd.strip()])
def Configure(cmd = '', pre = None):
    s = './configure'
    if pre:
        s = pre + ' ' + s
    s += ' --prefix=%s' % Prefix()
    if Option('build_host'):
        s += ' --host=%s' % Option('build_host')
    if cmd:
        s += ' ' + cmd
    if Option('configure_extra'):
        s += ' ' + Option('configure_extra')
    Execute(s)
def Append(fn, line):
    _instructions.append(['append', fn, line])
def Prepend(fn, line):
    _instructions.append(['prepend', fn, line])
def Copy(src, dst):
    _instructions.append(['copy', src.replace('//', '/'), dst.replace('//', '/')])
def Move(src, dst):
    _instructions.append(['move', src.replace('//', '/'), dst.replace('//', '/')])

class BuilderError: pass
def Error(s):
    print 'Builder error %s' % s
    raise BuilderError()
