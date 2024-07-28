from core.builder import *

def Versions():
    return ['4.5']

def Build():
    Extract(URL('http://sourceforge.net/projects/squashfs/files/squashfs/squashfs%s/squashfs%s.tar.gz' % (Ver(), Ver())))
    
    Chdir('squashfs-tools-%s' % Ver())
    Chdir('squashfs-tools')

    if Ver() == '4.2':
        Execute("sed -i.orig 's/FNM_EXTMATCH/0/; s/sysinfo.h/sysctl.h/; s/^inline/static inline/' mksquashfs.c unsquashfs.c")
        Append("xattr.h", "#define llistxattr(path, list, size) (listxattr(path, list, size, XATTR_NOFOLLOW))")
        Append("xattr.h", "#define lgetxattr(path, name, value, size) (getxattr(path, name, value, size, 0, XATTR_NOFOLLOW))")
        Append("xattr.h", "#define lsetxattr(path, name, value, size, flags) (setxattr(path, name, value, size, 0, flags | XATTR_NOFOLLOW))")

    if Option('fix_osx'):
        Execute("sed -i.orig 's/FNM_EXTMATCH/0/' action.c mksquashfs.c unsquashfs.c")
        Execute("sed -i.orig 's/sysinfo.h/sysctl.h/' unsquashfs.c")
        Execute("sed -i.orig 's:sigtimedwait:0;//:' unsquashfs_info.c")
        Execute("sed -i.orig 's:sigwaitinfo:0;//:' unsquashfs_info.c")
        Execute("sed -i.orig 's:sigtimedwait:0;//:' info.c")
        Execute("sed -i.orig 's:sigwaitinfo:0;//:' info.c")
        Execute("sed -i.orig 's:strdupa:strdup:' action.c")
        Append("xattr.h", "#define llistxattr(path, list, size) (listxattr(path, list, size, XATTR_NOFOLLOW))")
        Append("xattr.h", "#define lgetxattr(path, name, value, size) (getxattr(path, name, value, size, 0, XATTR_NOFOLLOW))")
        Append("xattr.h", "#define lsetxattr(path, name, value, size, flags) (setxattr(path, name, value, size, 0, flags | XATTR_NOFOLLOW))")
    tools = Prefix()
    #Make('LIBS=-L%s/lib INCLUDEDIR=-I%s/include mksquashfs' % (tools, tools))
    Make('LDFLAGS=-L%s/lib INCLUDEDIR=-I%s/include' % (tools, tools))
    Make('install INSTALL_DIR=%s/%s/bin' % (Dest(), Prefix()))
