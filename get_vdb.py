import os
import shutil
import sys
import urllib2
import zipfile


branch = 'master'


URL_ZIPFILE = 'https://github.com/jsbain/vdb/archive/%s.zip' % branch
TEMP_ZIPFILE = os.path.join(os.environ.get('TMPDIR', os.environ.get('TMP')),
                            'vdb_%s.zip' % branch)

print 'Downloading %s ...' % URL_ZIPFILE

try:
    u = urllib2.urlopen(URL_ZIPFILE)
    meta = u.info()
    try:
        file_size = int(meta.getheaders("Content-Length")[0])
    except IndexError:
        file_size = None
    with open(TEMP_ZIPFILE, 'wb') as outs:
        file_size_dl = 0
        block_sz = 8192
        while True:
            buf = u.read(block_sz)
            if not buf:
                break
            file_size_dl += len(buf)
            outs.write(buf)

except:
    sys.stderr.write('Download failed! Please make sure internet connection is available.\n')
    sys.exit(1)

BASE_DIR = os.path.expanduser('~')
TARGET_DIR = os.path.join(BASE_DIR, 'Documents/site-packages/vdb')
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
print 'Unzipping into %s ...' % TARGET_DIR

with open(TEMP_ZIPFILE, 'rb') as ins:
    try:
        zipfp = zipfile.ZipFile(ins)
        for name in zipfp.namelist():
            data = zipfp.read(name)
            name = name.split('vdb-%s/' % branch, 1)[-1]  # strip the top-level directory
            if name == '':  # skip top-level directory
                continue

            fname = os.path.join(TARGET_DIR, name)
            if fname.endswith('/'):  # A directory
                if not os.path.exists(fname):
                    os.makedirs(fname)
            else:
                fp = open(fname, 'wb')
                try:
                    fp.write(data)
                finally:
                    fp.close()
    except:
        sys.stderr.write('The zip file is corrupted. Pleases re-run the script.\n')
        sys.exit(1)



    print 'Installation completed.'


