from core.builder import *

def Versions():
    return ['3.5.0', '3.5.1', '3.6.0', '3.6.1', '3.9.1', '5.0.0']

def Build():
    v = Ver()

    m = Option('modules', 'cfe,compiler-rt').split(',')
    #m = Option('modules', 'cfe,compiler-rt,libcxx,libcxxabi,libunwind').split(',')

    for u in ['llvm'] + m:
        if u:
            Extract(URL('http://releases.llvm.org/%s/%s-%s.src.tar.xz' % (v, u, v)))

    if 'cfe' in m:
        Execute('mv cfe-%s.src llvm-%s.src/tools/clang' % (v, v))
    if 'compiler-rt' in m:
        Execute('mv compiler-rt-%s.src llvm-%s.src/projects/compiler-rt' % (v, v))

    Chdir('llvm-%s.src' % v)
    Mkdir('build')
    Chdir('build')

    cmd = 'cmake'

    cmd += ' -DCMAKE_INSTALL_PREFIX=' + Prefix()
    cmd += ' -DCMAKE_BUILD_TYPE=Release'
    cmd += ' "-DLLVM_TARGETS_TO_BUILD=ARM;X86"'

    if Option('shared'):
        cmd += ' -DBUILD_SHARED_LIBS=True'

    #cmd += ' -DLLVM_BUILD_LLVM_DYLIB=False'
    #cmd += ' -DLLVM_LINK_LLVM_DYLIBS=False'

    #cmd += ' -DCMAKE_CROSSCOMPILING=True'
    #cmd += ' -DLLVM_DEFAULT_TARGET_TRIPLE=arm-linux-gnueabihf'

    Execute(cmd + ' ..')

    Make()
    Make('install DESTDIR=%s' % Dest())

    if Option('default_cc'):
        Chdir("%s/%s" % (Dest(), Prefix()))
        Execute('ln -s clang bin/cc')
        Execute('ln -s clang bin/gcc')
        Execute('ln -s clang++ bin/c++')
        Execute('ln -s clang++ bin/g++')





