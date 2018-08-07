# Imports
import urllib
import urllib.request
from bs4 import BeautifulSoup


# Functions
def make_soup(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    return soup
