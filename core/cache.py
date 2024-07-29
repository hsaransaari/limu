import shelve, hashlib, os, pickle, atexit, time, urlverify
from contextlib import closing
import core

CACHE_FILE = os.getcwd() + '/' + 'limu.cache'

digest = hashlib.sha256

def hashStr(content):
    return digest(content).hexdigest()

def isHash(h):
    return type(h) == str and len(h) == 64

def hashFile(fn, store = True):
    sh = digest()
    f = open(fn, 'rb')
    while True:
        s = f.read(1024*1024)
        if not s:
            break
        sh.update(s)
    f.close()

    h = sh.hexdigest()
    if store:
        with closing(shelve.open(CACHE_FILE)) as db:
            db[h] = ('file', os.path.abspath(fn))
    return h

def hashResource(res):
    h = hashStr(res)
    with closing(shelve.open(CACHE_FILE)) as db:
        if h in db:
            return ('hash', h)

    core.shell.mkdir('resourcecache')

    fn = 'resourcecache/%s' % h
    f = open(fn, 'wb')
    f.write(res)
    f.close()

    h2 = hashFile(fn)
    assert h == h2

    return ('hash', h)

def hashInstructions(instructions):
    assert type(instructions) == list
    ret = hashStr(pickle.dumps(instructions))

    #time.sleep(0.1) # Avoid conflict with other prints
    print "HASHI %s %s" % (ret, str(instructions))
    return ret

def fetchURL(url, fn):
    localFile = 'filecache/%s' % fn

    h = hashStr(url)
    with closing(shelve.open(CACHE_FILE)) as db:
        if h in db and os.path.exists(localFile):
            return db[h]

    core.shell.mkdir('filecache')

    core.shell.shExec('curl -L -o %s "%s"' % (localFile + ".tmp", url))

    urlverify.verify(url, hashFile(localFile + ".tmp", False))

    core.shell.rename(localFile + '.tmp', localFile)

    with closing(shelve.open(CACHE_FILE)) as db:
        db[h] = ('hash', hashFile(localFile))
        return db[h]

def fetchLocalFile(url, fn):
    with closing(shelve.open(CACHE_FILE)) as db:
        h = hashStr(url)
        if h in db:
            return db[h]

        db[h] = ('hash', hashFile(url))
        return db[h]

def find(h):
    with closing(shelve.open(CACHE_FILE)) as db:
        if h in db:
            return db[h]

def hashToFile(h):
    assert isHash(h)
    with closing(shelve.open(CACHE_FILE)) as db:
        if h in db:
            entry = db[h]
            assert entry[0] == 'file'
            return entry[1]

def cacheExecution(instructions, h2):
    assert hashToFile(h2) != None
    h = hashInstructions(instructions)
    with closing(shelve.open(CACHE_FILE)) as db:
        db[h] = ('hash', h2)
