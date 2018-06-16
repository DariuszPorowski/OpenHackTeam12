import os

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(directory + ' created...')

from urllib.request import urlopen, urlretrieve

def get_lines_from_url(url):
    content = urlopen(url)
    lines = []
    for line in content:
        lines.append(line)
    return lines

def download_and_save_file(url, path):
    url = str(url).replace('b\'http', 'http').replace('\\r\\n\'', '')
    tokens = url.split('/')
    fileName = tokens[-1]
    urlretrieve(url, path + '/' + fileName)
    print('Azure --(' + fileName + ')--> ' + path)

def get_test_lines(fileName):
    lines = []
    with open(fileName, 'r') as textFile:
        for line in textFile:
            lines.append(line)
    return lines

imagesUrl = 'https://challenge.blob.core.windows.net/challengefiles/summit_post_urls_selected.txt'
basePath = './'
imagesPath = basePath + 'source'

create_directory_if_not_exists(imagesPath)

imageUrls = get_lines_from_url(imagesUrl)
for url in imageUrls:
    download_and_save_file(url, imagesPath)