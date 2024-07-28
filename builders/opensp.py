from core.builder import *

patch = """diff -ur yks/OpenSP-1.5.1/include/InternalInputSource.h kaks/OpenSP-1.5.1/include/InternalInputSource.h
--- yks/OpenSP-1.5.1/include/InternalInputSource.h	2003-07-17 21:14:00.000000000 +0300
+++ kaks/OpenSP-1.5.1/include/InternalInputSource.h	2015-05-30 13:35:16.209859873 +0300
@@ -34,7 +34,7 @@
   void pushCharRef(Char ch, const NamedCharRef &);
   Boolean rewind(Messenger &);
   const StringC *contents();
-  InternalInputSource *InternalInputSource::asInternalInputSource();
+  InternalInputSource *asInternalInputSource();
   ~InternalInputSource();
 private:
   InternalInputSource(const InternalInputSource &); // undefined
diff -ur yks/OpenSP-1.5.1/include/RangeMap.cxx kaks/OpenSP-1.5.1/include/RangeMap.cxx
--- yks/OpenSP-1.5.1/include/RangeMap.cxx	2000-02-25 18:55:21.000000000 +0200
+++ kaks/OpenSP-1.5.1/include/RangeMap.cxx	2015-05-30 13:36:07.713859461 +0300
@@ -7,6 +7,7 @@
 #include "RangeMap.h"
 #include "ISet.h"
 #include "types.h"
+#include "constant.h"
 
 #ifdef SP_NAMESPACE
 namespace SP_NAMESPACE {
"""
 
def Versions():
    return ['1.5.1']

def Build():
    Extract(URL('http://sourceforge.net/projects/openjade/files/opensp/%s/OpenSP-%s.tar.gz/download' % (Ver(), Ver()), 'OpenSP-%s.tar.gz' % Ver()))
    Chdir('OpenSP-%s' % Ver())
    File('patch.patch', patch)
    Execute('patch -p2 < patch.patch')
    Execute('./configure --prefix=%s' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
