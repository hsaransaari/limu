from core.builder import *

# Source: http://lists.gnu.org/archive/html/help-grub/2013-07/msg00055.html
patch = """--- grub-core/gnulib/stdio.in.h~
+++ grub-core/gnulib/stdio.in.h
@@ -140,9 +140,10 @@
 /* It is very rare that the developer ever has full control of stdin,
    so any use of gets warrants an unconditional warning.  Assume it is
    always declared, since it is required by C89.  */
+#if defined gets
 #undef gets
 _GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
-
+#endif
 #if @GNULIB_FOPEN@
 # if @REPLACE_FOPEN@
 #  if !(defined __cplusplus && defined GNULIB_NAMESPACE)
"""
#2012-09-17 19:30:25.951421145 +0100
#2012-09-17 19:30:25.965421146 +0100

def Versions():
    return ['2.00']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/grub/grub-%s.tar.gz' % Ver()))
    Chdir('grub-%s' % Ver())
    File('patch.patch', patch)
    Execute('patch -p0 < patch.patch')
    Execute('./configure --prefix=%s --disable-werror' % Prefix())
    Make()
    Make('install DESTDIR=%s' % Dest())
