from core.builder import *

def Versions():
    return ['2.44.1']

def Build():
    v = Ver().rsplit('.', 1)[0]
    Extract(URL('https://ftp.gnome.org/pub/gnome/sources/glib/%s/glib-%s.tar.xz' % (v, Ver())))
    Chdir('%s-%s' % (Builder(), Ver()))
    p = Prefix()

    if Option('test'):
        Configure('--disable-nls glib_cv_stack_grows=yes glib_cv_uscore=yes ac_cv_func_posix_getpwuid_r=no ac_cv_func_posix_getgrgid_r=no', 'CFLAGS="-I%s/include" LDFLAGS="-L%s/lib" ZLIB_CFLAGS=-I%s ZLIB_LIBS="-L%s -lz" LIBFFI_CFLAGS="-I%s -Wall" LIBFFI_LIBS=-lffi' % (p, p, p, p, p))
    else:
        Configure('CFLAGS="-I%s/include" LDFLAGS="-L%s/lib" ZLIB_CFLAGS=-I%s ZLIB_LIBS="-L%s -lz" LIBFFI_CFLAGS="-I%s -Wall" LIBFFI_LIBS=-lffi' % (p, p, p, p, p))
    #Execute('CFLAGS="-I%s/include" LDFLAGS="-L%s/lib" ZLIB_CFLAGS=-I%s ZLIB_LIBS="-L%s -lz" LIBFFI_CFLAGS="-I%s -Wall" LIBFFI_LIBS=-lffi ./configure --prefix=%s' % (p, p, p, p, p, p))
    Make('CFLAGS="-I%s/include -Wno-error=format-nonliteral"' % Prefix())
    Make('install DESTDIR=%s' % Dest())
