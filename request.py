from bs4 import BeautifulSoup
import requests
import gzip
import shutil
import os


def scrape_file_url(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    listings_gzs = []
    reviews_gzs = []
    for tag in soup.find_all('a'):
        link = tag.get('href')
        if link and 'san-francisco' in link and 'listings.csv.gz' in link:
            listings_gzs.append(link)
        elif link and 'san-francisco' in link and 'reviews.csv.gz' in link:
            reviews_gzs.append(link)

    listings_gzs.sort(reverse=True)
    reviews_gzs.sort(reverse=True)
    return listings_gzs[:45] + reviews_gzs[:45] # take only 45


def download(links):
    # download gzs
    for link in links:
        directory = './data/' + link.split('/')[-3] + '/'
        filename = link.split('/')[-1]
        r = requests.get(link, allow_redirects=True)

        if not os.path.exists(directory):
            os.makedirs(directory)

        open(directory + filename, 'wb').write(r.content)

        unzip_gz(directory, filename)


def unzip_gz(directory, filename):
    with gzip.open(directory + filename, 'rb') as f_in:
        with open(directory + filename.replace('.gz', ''), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


if __name__ == '__main__':
    links = scrape_file_url('http://insideairbnb.com/get-the-data.html')
    download(links)
