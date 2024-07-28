from core.builder import *

static_patch = """--- yks/unionfs-fuse-1.0/src/Makefile
+++ kaks/unionfs-fuse-1.0/src/Makefile
@@ -8,9 +8,9 @@
 # CPPFLAGS += -DDISABLE_XATTR # disable xattr support
 # CPPFLAGS += -DDISABLE_AT    # disable *at function support
 
-LDFLAGS += 
+LDFLAGS += -static
 
-LIB = $(shell pkg-config --libs fuse) -lpthread
+LIB = $(shell pkg-config --libs fuse) -lpthread -ldl
 
 HASHTABLE_OBJ = hashtable.o hashtable_itr.o
 UNIONFS_OBJ = unionfs.o opts.o debug.o findbranch.o readdir.o \\
"""

def Versions():
    return ['1.0']

def Build():
    Extract(URL('https://github.com/rpodgorny/unionfs-fuse/archive/v%s.tar.gz' % Ver(), 'unionfs-fuse-%s.tar.gz' % Ver()))
    Chdir('unionfs-fuse-%s' % Ver())
    File('static.patch', static_patch)
    Execute('patch -p2 < static.patch')
    Make()
    Make('install PREFIX=%s DESTDIR=%s' % (Prefix(), Dest()))
