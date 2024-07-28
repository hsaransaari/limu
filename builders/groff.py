from core.builder import *

# https://savannah.gnu.org/bugs/index.php?43581
patch = """
diff --git a/Makefile.in b/Makefile.in
index bc156ce..70c6f85 100644
--- a/Makefile.in
+++ b/Makefile.in
@@ -896,6 +896,8 @@ $(GNULIBDIRS): FORCE
 	  $(MAKE) ACLOCAL=: AUTOCONF=: AUTOHEADER=: AUTOMAKE=: $(do) ;; \
 	esac
 
+$(SHPROGDIRS): $(PROGDEPDIRS)
+
 $(OTHERDIRS): $(PROGDEPDIRS) $(CCPROGDIRS) $(CPROGDIRS) $(SHPROGDIRS)
 
 $(INCDIRS) $(PROGDEPDIRS) $(SHPROGDIRS) $(OTHERDIRS): FORCE
"""

def Versions():
    return ['1.22.3']

def Build():
    Extract(URL('ftp://ftp.gnu.org/pub/gnu/%s/%s-%s.tar.gz' % (Builder(), Builder(), Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    File('patch.patch', patch)
    Execute('patch -p1 < patch.patch')
    Configure()
    Make('-j1')
    Make('install DESTDIR=%s' % Dest())
