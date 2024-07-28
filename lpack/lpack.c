// This is lpack, limu packer. It packs and unpacks directories in .tar.gz
// format. The idea is to 1) canonicalize packages by removing user ids and
// timestamps and 2) provide same interface for all platforms regardless of the
// tar implementation. This file is public domain.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <dirent.h>
#include <limits.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <libgen.h>
#include <zlib.h>

enum Mode
{
    NONE,
    EXTRACT,
    CREATE
};

static int dryRun;
static int verbose;
static enum Mode operationMode;
static FILE* inputStream;
static FILE* outputStream;
static const char* destinationPath;
static const char* sourcePath;
static const char* filterPath;
static int compressLevel = 1;

static void errorf(const char* fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    fprintf(stderr, "fatal: ");
    vfprintf(stderr, fmt, args);
    fprintf(stderr, "\n");
    va_end(args);
    exit(EXIT_FAILURE);
}

// Extract.

struct Header
{
    char name[100];
    char mode[8];
    char uid[8];
    char gid[8];
    char size[12];
    char mtime[12];
    char chksum[8];
    char link[1];
    char linkname[100];
    char magic[6];
    char version[2];
    char uname[32];
    char gname[32];
    char devmajor[8];
    char devminor[8];
    char prefix[155];
};

static int octalToInt(int ch)
{
    if (ch < '0' || ch > '7')
        errorf("bad octal\n");
    return ch - '0';
}

static uint64_t parseOctal(const char* ptr, int m)
{
    uint64_t ret = 0;
    int i;
    for (i = 0; i < m; i++)
    {
        if (ptr[i] == 0 || ptr[i] == ' ')
            break;
        ret <<= 3;
        ret |= octalToInt(ptr[i]);
    }
    return ret;
}

static size_t parseSize(const struct Header* hdr)
{
    return (size_t)parseOctal(hdr->size, 12);
}

static uint32_t parseMode(const struct Header* hdr)
{
    return (uint32_t)parseOctal(hdr->mode, 8);
}

static int isEmptyBlock(uint8_t* block)
{
    int i;
    for (i = 0; i < 512; i++)
        if (block[i])
            return 0;
    return 1;
}

static z_stream zInputStream;
static uint8_t zInputStreamInput[64*1024];

static void readBlock(uint8_t* destBuffer)
{
    zInputStream.avail_out = 512;
    zInputStream.next_out = destBuffer;

    while (zInputStream.avail_out > 0)
    {
        if (zInputStream.avail_in == 0)
        {
            zInputStream.avail_in = fread(zInputStreamInput, 1, sizeof(zInputStreamInput), inputStream);
            if (ferror(inputStream))
                errorf("error reading input");

            if (zInputStream.avail_in == 0)
                errorf("unexpected eof");

            zInputStream.next_in = zInputStreamInput;
        }

        int ret = inflate(&zInputStream, Z_NO_FLUSH);
        if (ret != Z_OK && ret != Z_STREAM_END)
            errorf("zlib inflate() failed %d", ret);
    }
}

static void extract()
{
    if (!destinationPath)
        errorf("destination directory not specified");

    // Get input stream.

    if (inputStream && sourcePath)
        errorf("both input stream and source path specified");

    if (!inputStream)
    {
        if (!sourcePath)
            errorf("input not specified");

        inputStream = fopen(sourcePath, "rb");
        if (!inputStream)
            errorf("cannot open input %s", sourcePath);
    }

    // Initialize output directory.

    char destdir[PATH_MAX+2];

    if (!dryRun)
    {
        mkdir(destinationPath, 0777);

        if (!realpath(destinationPath, destdir))
            errorf("cannot resolve destination directory");

        if (destdir[strlen(destdir)-1] != '/')
            strcat(destdir, "/");
    }
    else
    {
        strcpy(destdir, destinationPath);
        strcat(destdir, "/");
    }

    if (verbose)
        fprintf(stderr, "destination directory: %s\n", destdir);

    // Initialize inflate.

    memset(&zInputStream, 0, sizeof(zInputStream));
    if (inflateInit2(&zInputStream, 31) != Z_OK)
        errorf("zlib inflateInit() failed");

    // Process tar.

    uint8_t block[512];

    for (;;)
    {
        readBlock(block);

        if (isEmptyBlock(block))
        {
            readBlock(block);
            if (isEmptyBlock(block))
                return;

            errorf("expecting header but got empty block");
        }

        struct Header* hdr = (struct Header*)&block[0];
        hdr->name[99] = 0;
        hdr->prefix[154] = 0;
        if (strncmp(hdr->magic, "ustar", 6) != 0)
            hdr->prefix[0] = 0;

        size_t size = parseSize(hdr);
        uint32_t mode = parseMode(hdr);

        // Skip extended header.

        if (hdr->link[0] == 'x')
        {
            size_t s;
            for (s = 0; s < size; s += 512)
                readBlock(block);
            continue;
        }

        // Get suggested name.

        char origname[PATH_MAX*2+1];
        strcpy(origname, destdir);
        if (hdr->prefix[0] != 0)
        {
            strcat(origname, hdr->prefix);
            strcat(origname, "/");
        }
        strcat(origname, hdr->name);

        char dirdata[PATH_MAX*2+1];
        strcpy(dirdata, origname);
        const char* dir = dirname(dirdata);

        if (!dryRun)
        {
            char name[PATH_MAX+1];
            if (!realpath(dir, name))
                errorf("bad directory %s for %s", dir, origname);

            if (strncmp(name, destdir, strlen(destdir)-1) != 0)
                errorf("destination not allowed %s %s", origname, dir);
        }

        //realpath(origname, name)

        const char* path = origname;

        if (hdr->link[0] == 0 || hdr->link[0] == '0')
        {
            if (!dryRun)
                unlink(origname);

            if (verbose)
                fprintf(stderr, "file %s %o %d\n", path, mode, (int)size);

            FILE* fp = NULL;
            if (!dryRun)
            {
                fp = fopen(origname, "wb");
                if (!fp)
                    errorf("cannot open %s for writing", origname);
            }

            size_t s;
            for (s = 0; s < size; s += 512)
            {
                readBlock(block);
                size_t s2 = (size - s < 512) ? size - s : 512;
                if (!dryRun)
                    fwrite(block, s2, 1, fp);
            }

            if (!dryRun)
                fclose(fp);
        }
        else if (hdr->link[0] == '2')
        {
            if (!dryRun)
                unlink(origname);

            if (size != 0)
                errorf("symlink has size");

            if (!dryRun)
            {
                if (symlink(hdr->linkname, origname) != 0)
                {
                    if (errno == EEXIST)
                    {
                        if (unlink(origname) != 0)
                            errorf("cannot remove original %s: %s", origname, strerror(errno));

                        if (verbose)
                            fprintf(stderr, "remove original file %s\n", origname);

                        if (symlink(hdr->linkname, origname) != 0)
                            errorf("cannot create symlink %s: %s", origname, strerror(errno));
                    }
                }
            }

            if (verbose)
                fprintf(stderr, "link %s => %s\n", path, hdr->linkname);
        }
        else if (hdr->link[0] == '5')
        {
            if (!dryRun)
                unlink(origname);

            if (size != 0)
                errorf("directory has size");

            if (!dryRun && mkdir(origname, mode) != 0)
            {
                if (errno != EEXIST)
                    errorf("cannot create directory %s", origname);
            }

            if (verbose)
                fprintf(stderr, "directory %s\n", path);
        }
        else
            errorf("unhandled file %s type %c", path, hdr->link[0]);

        if (!dryRun)
        {
            // TODO: chmod should be done after all directories have been created
            if (hdr->link[0] != '2')
                if (chmod(origname, mode) != 0)
                    errorf("cannot chmod %s to %d", origname, mode);
        }
    }
}

// Create.

static z_stream zOutputStream;
static uint8_t zOutputStreamBuffer[64*1024];

static void writeBlock(const uint8_t* srcBuffer, int flush)
{
    zOutputStream.next_in = (void*)srcBuffer;
    zOutputStream.avail_in = 512;

    do
    {
        zOutputStream.next_out = zOutputStreamBuffer;
        zOutputStream.avail_out = sizeof(zOutputStreamBuffer);
        deflate(&zOutputStream, flush ? Z_FINISH : Z_NO_FLUSH);
        fwrite(zOutputStreamBuffer, 1, sizeof(zOutputStreamBuffer) - zOutputStream.avail_out, outputStream);
    } while (zOutputStream.avail_out == 0);
}

struct File
{
    char name[PATH_MAX+1];
    struct File* next;
};

static int fileCompare(const void* a_, const void* b_)
{
    const struct File*const* a = a_;
    const struct File*const* b = b_;
    return strcmp((*a)->name, (*b)->name);
}

static void recursiveCreate(const char* tarPath, const char* hostPath)
{
    struct File* firstFile = NULL;

    // Read all files.

    DIR* dir = opendir(hostPath);
    if (!dir)
        errorf("cannot open directory %s", hostPath);

    struct File** next = &firstFile;

    for (;;)
    {
        struct dirent* de = readdir(dir);
        if (!de)
            break;

        if (strcmp(de->d_name, ".") == 0 || strcmp(de->d_name, "..") == 0)
            continue;

        *next = malloc(sizeof(struct File));
        memset(*next, 0, sizeof(struct File));
        strcpy((*next)->name, de->d_name);
        next = &(*next)->next;
    }

    closedir(dir);

    // Sort.

    int cnt = 0;
    struct File* file;
    for (file = firstFile; file; file = file->next)
        cnt++;

    struct File** sortedFiles = malloc(sizeof(struct File*) * cnt);
    cnt = 0;
    for (file = firstFile; file; file = file->next)
        sortedFiles[cnt++] = file;

    qsort(sortedFiles, cnt, sizeof(void*), fileCompare);

    // Write and recurse.

    int i;
    for (i = 0; i < cnt; i++)
    {
        char hostPath2[PATH_MAX*2+1];
        strcpy(hostPath2, hostPath);
        strcat(hostPath2, "/");
        strcat(hostPath2, sortedFiles[i]->name);

        char tarPath2[PATH_MAX*2+1];
        strcpy(tarPath2, tarPath);
        strcat(tarPath2, "/");
        strcat(tarPath2, sortedFiles[i]->name);

        free(sortedFiles[i]);

        struct stat st;
        if (lstat(hostPath2, &st) != 0)
            errorf("cannot stat %s", hostPath2);

        if (verbose)
            fprintf(stderr, "entry %s as %s %o\n", hostPath2, tarPath2, st.st_mode);

        uint8_t block[512];
        memset(block, 0, sizeof(block));
        struct Header* hdr = (struct Header*)&block[0];

        assert(strlen(tarPath2) < 255);

        strcpy(hdr->magic, "ustar");
        memcpy(hdr->version, "00", 2);
        hdr->prefix[0] = 0;

        if (strlen(tarPath2) >= 100)
        {
            int i, len = strlen(tarPath2);
            for (i = len - 99; i < len; i++)
                if (tarPath2[i] == '/')
                    break;

            if (i >= len)
                errorf("bad path for tar %s", tarPath2);

            tarPath2[i] = 0;
            strcpy(hdr->prefix, tarPath2);
            strcpy(hdr->name, tarPath2+i+1);
            tarPath2[i] = '/';
        }
        else
            strcpy(hdr->name, tarPath2);
        sprintf(hdr->mode, "%06o", st.st_mode & 0777);
        sprintf(hdr->size, "%011o", (unsigned int)st.st_size);
        sprintf(hdr->size, "%011o", (unsigned int)st.st_size);

        memcpy(hdr->chksum, "        ", 8);

        if (S_ISREG(st.st_mode))
        {
            hdr->link[0] = '0';
        }
        else if (S_ISDIR(st.st_mode))
        {
            hdr->link[0] = '5';
            strcat(hdr->name, "/");
            sprintf(hdr->size, "%011o", 0);
        }
        else if (S_ISLNK(st.st_mode))
        {
            hdr->link[0] = '2';
            readlink(hostPath2, hdr->linkname, sizeof(hdr->linkname));
            sprintf(hdr->size, "%011o", 0);
        }
        else
            errorf("unknown file type %s %o", hostPath, st.st_mode);

        uint32_t checksum = 0;
        int i;
        for (i = 0; i < 512; i++)
            checksum += block[i];

        sprintf(hdr->chksum, "%06o", checksum);

        writeBlock(block, 0);

        // Write data.

        if (S_ISREG(st.st_mode))
        {
            FILE* fp = fopen(hostPath2, "rb");
            if (!fp)
                errorf("cannot open %s for reading", hostPath2);

            size_t s;
            for (s = 0; s < st.st_size; s += 512)
            {
                memset(block, 0, sizeof(block));
                size_t ret = fread(block, 1, 512, fp);
                if (ret != ((st.st_size - s) < 512 ? st.st_size-s : 512))
                    errorf("cannot read %s at %d of %d (read only %d)", hostPath2, s, st.st_size, ret);
                writeBlock(block, 0);
            }

            fclose(fp);
        }

        if (S_ISDIR(st.st_mode))
            recursiveCreate(tarPath2, hostPath2);
    }

    free(sortedFiles);
}

static void create()
{
    if (inputStream)
        errorf("create from stdin not supported");

    if (!sourcePath)
        errorf("source directory not specified");

    if (outputStream && destinationPath)
        errorf("both output stream and destination path specified");

    if (!outputStream)
    {
        if (!destinationPath)
            errorf("output not specified");

        if (!dryRun)
        {
            outputStream = fopen(destinationPath, "wb");
            if (!outputStream)
                errorf("cannot open output %s", destinationPath);
        }
    }

    memset(&zOutputStream, 0, sizeof(zOutputStream));
    if (deflateInit2(&zOutputStream, compressLevel, 8, 31, 8, Z_DEFAULT_STRATEGY) != Z_OK)
        errorf("zlib deflateInit() failed");

    recursiveCreate(".", sourcePath);

    uint8_t block[512];
    memset(block, 0, sizeof(block));
    writeBlock(block, 0);
    writeBlock(block, 1);
}

// Main.

int main(int argc, char* argv[])
{
    int i;
    for (i = 1; i < argc; i++)
    {
        if (strcmp(argv[i], "--extract") == 0)
            operationMode = EXTRACT;
        else if (strcmp(argv[i], "--create") == 0)
            operationMode = CREATE;
        else if (strcmp(argv[i], "--source") == 0)
            sourcePath = argv[++i];
        else if (strcmp(argv[i], "--destination") == 0)
            destinationPath = argv[++i];
        else if (strcmp(argv[i], "--filter") == 0)
            filterPath = argv[++i];
        else if (strcmp(argv[i], "--dry-run") == 0)
            dryRun = 1;
        else if (strcmp(argv[i], "--input-stdin") == 0)
            inputStream = stdin;
        else if (strcmp(argv[i], "--output-stdout") == 0)
            outputStream = stdout;
        else if (strcmp(argv[i], "--verbose") == 0)
            verbose = 1;
        else if (strcmp(argv[i], "--fast") == 0)
            compressLevel = 1;
        else if (strcmp(argv[i], "--best") == 0)
            compressLevel = 9;
        else if (strcmp(argv[i], "--version") == 0)
        {
            printf("lpack 0.1\n");
            return EXIT_SUCCESS;
        }
        else
            errorf("bad argument %s", argv[i]);
    }

    if (operationMode == EXTRACT)
        extract();
    else if (operationMode == CREATE)
        create();
    else
    {
        errorf("operation mode not specified");
    }

    // Clean-up.

    if (inputStream && inputStream != stdin)
        fclose(inputStream);

    if (outputStream && outputStream != stdout)
        fclose(outputStream);

    return EXIT_SUCCESS;
}
