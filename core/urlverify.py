import shelve, os, pickle, atexit
import core

ACCEPT_NON_VERIFIED_URLS = False

urlToHash = {}
hashToUrl = {}

def insert(url, h):
    pass

def add_verified_url(url, h):
    assert len(url.split()) == 1

    load()

    assert not url in urlToHash
    urlToHash[url] = h
    hashToUrl.setdefault(h, [])
    hashToUrl[h].append(url)

    f = open('verified_urls.dat', 'a')
    print '%s %s\n' % (h, url)
    f.close()

def load():
    global urlToHash, hashToUrl
    urlToHash = {}
    hashToUrl = {}

    try:
        f = open('verified_urls.dat', 'r')
    except:
        return

    for line in f.read().splitlines():
        s = line.split()
        h, url = s

        assert not url in urlToHash
        urlToHash[url] = h
        hashToUrl.setdefault(h, [])
        hashToUrl[h].append(url)

    f.close()

def verify(url, h):
    if len(url.split()) != 1:
        print 'url is not verifiable %s' % url
        if not ACCEPT_NON_VERIFIED_URLS:
            raise RuntimeError('url %s is not verifiable' % url)
        return

    if not urlToHash:
        load()

    if not url in urlToHash:
        print 'cannot verify url: %s' % url
        f = open('latest_unverified_url.dat', 'w')
        f.write('%s %s\n' % (h, url))
        f.close()
        if not ACCEPT_NON_VERIFIED_URLS:
            raise RuntimeError('url %s not verified, check latest_unverified_url.dat and execute ./verify_latest_url.sh' % url)
        return

    if urlToHash[url] != h:
        raise RuntimeError('url %s has hash %s expecting %s' % (url, h, urlToHash[url]))
