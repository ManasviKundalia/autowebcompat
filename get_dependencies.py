import sys
import os
import tarfile
from zipfile import ZipFile
import requests
from rfc6266 import parse_requests_response


def download(url):
    response = requests.get(url)

    try:
        cd = response.headers['content-disposition']
        extnsn = cd[cd.rfind('.')+1:]
        filename = parse_requests_response(response).filename_sanitized(extnsn)   
    except:
        #get base name of file from url
        filename = url[url.rfind('/')+1:url.find('?')] 
        if filename.rfind('.')==-1:     #check for valid filenames
            print('Couldn\'t get filename for this url')
            return
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                sys.stdout.flush()
                sys.stdout.write('\n')
    return filename
    return filename


if sys.platform.startswith('linux'):
    url = 'https://www.dropbox.com/s/ziti4nkdzhgwg1n/linux.tar.xz?dl=1'
elif sys.platform.startswith('darwin'):
    url = 'https://www.dropbox.com/s/k4yifantsypy9xv/mac.tar.xz?dl=1'
elif sys.platform.startswith('win32'):
    url = 'https://www.dropbox.com/s/xskj9rpn2fjkra8/win32.tar.xz?dl=1'

print('[*] Downloading support files...')
#download(url, name)
name = download(url)
try:
    print('[*] Extracting files...')
    with tarfile.open(name, 'r:xz') as f:
        f.extractall('.')
    os.remove(name)
except:
    print('bad url')
    
print('[*] Downloading data.zip...')
download('https://www.dropbox.com/s/7f5uok2alxz9j1r/data.zip?dl=1')

print('[*] Extracting data.zip...')
try:
    with ZipFile('data.zip', 'r') as z:
        z.extractall()
except BadZipfile:
    print('BAD ZIP FILE')

os.remove('data.zip')
print('[*] Completed!')
