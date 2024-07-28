from core.builder import *

patch = """diff -ur yks/sp-1.3.4/include/config.h kaks/sp-1.3.4/include/config.h
--- yks/sp-1.3.4/include/config.h	1999-10-13 08:02:46.000000000 +0300
+++ kaks/sp-1.3.4/include/config.h	2015-05-30 13:13:56.413870131 +0300
@@ -26,7 +26,7 @@
 #endif
 #if __GNUC__ > 2 || (__GNUC__ == 2 && __GNUC_MINOR__ >= 8)
 #define SP_ANSI_LIB
-#define SP_NO_STD_NAMESPACE
+//#define SP_NO_STD_NAMESPACE
 #undef SP_NEW_H_MISSING
 #endif
 
diff -ur yks/sp-1.3.4/include/RangeMap.h kaks/sp-1.3.4/include/RangeMap.h
--- yks/sp-1.3.4/include/RangeMap.h	1998-10-09 08:08:59.000000000 +0300
+++ kaks/sp-1.3.4/include/RangeMap.h	2015-05-30 13:03:06.149875342 +0300
@@ -54,6 +54,7 @@
   }
 private:
   size_t count_;
+#undef typename
   typename Vector<RangeMapRange<From,To> >::const_iterator ptr_;
 };
 
"""

def Versions():
    return ['1.3.4']

def Build():
    Extract(URL('ftp://ftp.jclark.com/pub/%s/%s-%s.tar.gz' % (Builder(), Builder(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    File('patch.patch', patch)
    Execute('patch -p2 < patch.patch')
    Execute('make')
    Make()
    Make('install prefix=%s' % Dest())
