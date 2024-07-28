from core.builder import *

def Versions():
    return ['0.1']

def Build():
    if Option('cross'):
        Execute('export CC=%s-gcc' % Option('cross'))
        Execute('export CXX=%s-gcc' % Option('cross'))

    Append('jelly.c', "#include <stdio.h>")
    Append('jelly.c', "int main() { printf(\"Hello.\\n\"); return 0; }")
    Execute("$CC -o jelly jelly.c")
    Execute("./jelly")
    Mkdir("%s/%s" % (Dest(), Prefix()))
    Copy('jelly', "%s/%s" % (Dest(), Prefix()))
