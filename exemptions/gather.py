# Imports
import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


# Functions

def get_extension_from_href_ending(soup, endings, identifier, get_title = True, title = '', print_interim=True):
    retrieved_links = {}
    for link in soup.find_all('a'):
        if link.get('href'):
            current_link = link.get('href')
            if get_title:
                title = link.get('title')
            else:
                title = title
            if any([current_link.endswith(ending) for ending in endings]) and title and 'ISD' in title:
                if print_interim:
                    print(title, current_link)
                retrieved_links[title] = (current_link, identifier)
    return retrieved_links


def get_extension_from_href_contains(soup, containing, identifier, get_title = True, title = '', debug_string=None, print_interim=True):
    retrieved_links = {}
    for link in soup.find_all('a'):
        if link.get('href'):
            current_link = link.get('href')
            if get_title:
                title = link.get('title')
            else:
                title = title
            if any(strng in current_link for strng in containing) and title and 'ISD' in title:
                if print_interim:
                    print(debug_string, title, current_link)
                retrieved_links[title] = (current_link, identifier)
    return retrieved_links


###
#   Classes
###
# TODO Gather docs needs to search scripts and iframes.
class DocLinks:
    """This will be a class for the first level of districts and links"""

    def __init__(self, url, print_interim=True):
        self.html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(self.html)
        self.doc_links = {}
        self._get_docs(print_interim)
        self.docs_df = pd.DataFrame.from_dict(self.doc_links,
                                              orient='index',
                                              columns=['link', 'type'])

    def _get_docs(self, print_interim):
        # Word Docs
        docx_links = get_extension_from_href_ending(soup=self.soup,
                                                    endings=['docx', 'doc'],
                                                    identifier='docx',
                                                    print_interim=print_interim)
        self.doc_links.update(docx_links)

        # PDFs
        pdf_links = get_extension_from_href_ending(soup=self.soup,
                                                   endings=['.pdf'],
                                                   identifier='pdf',
                                                   print_interim=print_interim)

        self.doc_links.update(pdf_links)

        #  Google Docs
        google_links = get_extension_from_href_contains(self.soup,
                                                        ['drive.google.com'],
                                                        identifier='google',
                                                        print_interim=print_interim)
        self.doc_links.update(google_links)

class SeedLinks:
    """Seed links for web crawler"""

    def __init__(self, url, print_interim=True):
        self.seed_links = {}
        self.html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(self.html)
        self._get_seed_links(print_interim=print_interim)

    def _get_seed_links(self, print_interim=True):
        seed_links = {}
        for link in self.soup.find_all('a'):
            if link.get('href'):
                current_link = link.get('href')
                title = link.get('title')
                if ('http' in current_link
                        and title
                        and "ISD" in title
                        and not current_link.endswith('doc')
                        and '.pdf' not in current_link
                        and not current_link.endswith('docx')
                        and 'drive.google' not in current_link):
                    seed_links[title] = current_link
                if print_interim:
                    print(title, current_link)
        self.seed_links = seed_links



