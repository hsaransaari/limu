import os
import core, core.shell

def GenericPrepareParams(params):
    params.setdefault('prefix', '/usr')
    if params.get('host_tools', None):
        params['host_tools_path'] = os.getcwd() + '/tools'
    if params.get('cross', None) and not 'cross_target' in params:
        params['cross_target'] = params['cross'].split('/')[-1]
    return params

def GenericPrepareInstructions(params, instructions):
    out = []

    if params.get('host_tools', None):
        for t in params['host_tools'].split(','):
            out.append(['host_tool', ('hash', t)])

    if params.get('cross', None):
        c = params.get('cross')
        out.append(['env', 'CC',     '%s-gcc' % c])
        out.append(['env', 'CXX',    '%s-g++' % c])
        out.append(['env', 'AR',     '%s-ar' % c])
        out.append(['env', 'RANLIB', '%s-ranlib' % c])
        out.append(['env', 'CPP',    '%s-cpp' % c])

    out.extend(instructions)
    return out 

def GenericExecute(instructions):
    out = []
    hostTools = []

    for i in instructions:
        if i[0] == 'host_tool':
            assert i[1][0] == 'hash'
            hostTools.append(i[1][1])
        else:
            out.append(i)

    instructions[:] = out

    core.shell.remove('tools/')
    if hostTools:
        os.environ['PATH'] = os.getcwd() + '/tools/bin:' + os.getenv('PATH')
        core.makeHostTools(hostTools)
