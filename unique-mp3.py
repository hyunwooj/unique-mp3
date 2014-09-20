import argparse

from hashlib import md5
from os import listdir
from os.path import isfile, join
from shutil import copyfile

from mutagen.easyid3 import EasyID3


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dst', help='dest directory')
    parser.add_argument('src', help='source directories', nargs='+')

    args = parser.parse_args()

    files = []
    for path in args.src:
        files.extend([join(path, f) for f in listdir(path) if isfile(join(path, f))])

    digests = []
    total = 0
    duplicated = {}
    result = 0
    for f in files:
        try:
            tag = EasyID3(f)
        except:
            continue
        total += 1
        m = md5()
        m.update(tag['title'][0].encode('utf-8'))
        m.update(tag['artist'][0].encode('utf-8'))
        if m.digest() in digests:
            duplicated[str(m.digest())] = True
            continue
        digests.append(m.digest())
        dst = join(args.dst, '%s - %s.mp3' % (tag['artist'][0].replace('/', ''), tag['title'][0].replace('/', '')))
        copyfile(f, dst),
        result += 1
    print(len(duplicated), 'files duplicated')
    print(total, '->', result)
