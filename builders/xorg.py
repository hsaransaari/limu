from core.builder import *

xorgserver_patch = """From 21b896939c5bb242f3aacc37baf12379e43254b6 Mon Sep 17 00:00:00 2001
From: Egbert Eich <eich@freedesktop.org>
Date: Tue, 3 Mar 2015 16:27:05 +0100
Subject: symbols: Fix sdksyms.sh to cope with gcc5

Gcc5 adds additional lines stating line numbers before and
after __attribute__() which need to be skipped.

Signed-off-by: Egbert Eich <eich@freedesktop.org>
Tested-by: Daniel Stone <daniels@collabora.com>
Signed-off-by: Peter Hutterer <peter.hutterer@who-t.net>

diff --git a/hw/xfree86/sdksyms.sh b/hw/xfree86/sdksyms.sh
index 2305073..05ac410 100755
--- a/hw/xfree86/sdksyms.sh
+++ b/hw/xfree86/sdksyms.sh
@@ -350,13 +350,25 @@ BEGIN {
     if (sdk) {
 	n = 3;
 
+        # skip line numbers GCC 5 adds before __attribute__
+        while ($n == "" || $0 ~ /^# [0-9]+ "/) {
+           getline;
+           n = 1;
+        }
+
 	# skip attribute, if any
 	while ($n ~ /^(__attribute__|__global)/ ||
 	    # skip modifiers, if any
 	    $n ~ /^\*?(unsigned|const|volatile|struct|_X_EXPORT)$/ ||
 	    # skip pointer
-	    $n ~ /^[a-zA-Z0-9_]*\*$/)
+	    $n ~ /^[a-zA-Z0-9_]*\*$/) {
 	    n++;
+            # skip line numbers GCC 5 adds after __attribute__
+            while ($n == "" || $0 ~ /^# [0-9]+ "/) {
+               getline;
+               n = 1;
+            }
+        }
 
 	# type specifier may not be set, as in
 	#   extern _X_EXPORT unsigned name(...)
-- 
cgit v0.10.2
"""

def Versions():
    return ['7.7']

def Build():
    p = Option('pkg')
    if p.startswith('xf86-video-'):
        Extract(URL('https://www.x.org/releases/individual/driver/%s.tar.bz2' % p))
        #Extract(URL('https://www.x.org/archive/individual/src/everything/%s.tar.bz2' % (Ver(), p)))
    else:
        Extract(URL('https://www.x.org/releases/X11R%s/src/everything/%s.tar.bz2' % (Ver(), p)))
    Chdir('%s' % p)
    if p.startswith('xorg-server-'):
        File('patch.patch', xorgserver_patch)
        Execute('patch -p1 < patch.patch')
    Configure()
    Make('install DESTDIR=%s' % Dest())
