import urllib.request

def download_file(url):
    # get the file name from the url
    file_name = url.split('/')[-1]
    # download the file from the url
    urllib.request.urlretrieve(url, file_name)
    print('File', file_name, 'downloaded successfully.')

if __name__ == '__main__':
    file_url = input('Enter the URL of the file to download: ')
    download_file(file_url)
