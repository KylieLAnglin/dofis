# Imports
import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin


# Functions

def get_doc_links_from_href(url, strings_of_interest, identifier, get_title=True, title='', print_interim=True,
                            kind='ending'):
    """
    First level links

    Takes url and extracts hrefs of interest.
    :param url: url to search for document links
    :param strings_of_interest:  Indicate type of documents with strings like .pdf
    :param identifier: By what name will you identify these document types?
    :param get_title: Do you want to find the link title inside the href or provide a title? False = provide title.
    :param title: If providing title, what is it? This should be a district name.
    :param print_interim: Want to print interim output?
    :param kind: -- Where to look for string in href (default: 'ending', alternative 'containing')
    :return: dic Returns the following dictionary: {title: (link, type)}
    """

    soup = make_soup(url=url)
    retrieved_links = {}
    for link in soup.find_all('a'):
        if link.get('href'):
            current_link = link.get('href')
            if get_title:
                title = link.get('title')
            else:
                title = title

            # Intelligently route the condition for filtering links based on the kind argument
            condition_mapping = {
                'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                'contains': [strng in current_link for strng in strings_of_interest],
            }
            condition = condition_mapping[kind]

            if any(condition) and title and 'ISD' in title:
                if print_interim:
                    print(title, current_link)
                retrieved_links[title] = (current_link, identifier)
    return retrieved_links


def get_doc_links_from_href_scripts_iframes(url, identifier, title, strings_of_interest, kind):

    """
    Second level links

    Takes url and extracts docs from hrefs, scripts, and iframes
    :param url: url to search for document links
    :param strings_of_interest: Indicate types of documents with strings of interest like .pdf
    :param identifier: By what name will you identify these document types?
    :param title: District name
    :param kind: -- Where to look for string in href (default: 'ending', alternative 'containing')
    :return: dic Returns the following dictionary: {link: (title, type)}
    """
    retrieved_links = {}
    try:
        soup = make_soup(url)
        for link in soup.find_all('a'):
            current_link = link.get('href')
            current_link = clean_link(url=url, current_link=current_link)
            condition_mapping = {
                'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                'contains': [strng in current_link for strng in strings_of_interest],
            }
            condition = condition_mapping[kind]
            if any(condition):
                retrieved_links[current_link] = (title, identifier)
        # TODO <- Figure out how to gracefully handle iframes without src attributes
        for iframe in soup.find_all('iframe'):
            current_link = iframe.attrs['src']
            current_link = clean_link(url=url, current_link=current_link)
            condition_mapping = {
                'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                'contains': [strng in current_link for strng in strings_of_interest],
            }
            condition = condition_mapping[kind]
            if any(condition):
                retrieved_links[current_link] = (title, identifier)
        for script in soup.find_all('script'):
            string = str(script)
            matches = re.findall(r'"(.*)"', string)  # figure out what we're looking for here
            for match in matches:
                current_link = match
                current_link = clean_link(url=url, current_link=current_link)
                condition_mapping = {
                    'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                    'contains': [strng in current_link for strng in strings_of_interest],
                }
                condition = condition_mapping[kind]
                if any(condition):
                    retrieved_links[current_link] = (title, identifier)
    except Exception as e:
        print('error:', title, e)
    return retrieved_links


def clean_link(url, current_link):
    if not current_link:
        current_link = ''
    if not current_link.startswith('http') and not current_link.startswith('www'):
        current_link = urljoin(url, current_link)
    if " " in current_link:
        current_link = current_link.replace(" ", "%20")
    return current_link


def make_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup


###
#   Classes
###
class FirstLevelLinks:
    """This will be a class for the first level of districts and links"""

    def __init__(self, url, print_interim=True):
        self.doc_links = {}
        self._get_docs(url, print_interim)
        self.docs_df = pd.DataFrame.from_dict(self.doc_links,
                                              orient='index',
                                              columns=['link', 'type'])

    def _get_docs(self, url, print_interim):
        # Word Docs
        docx_links = get_doc_links_from_href(url=url,
                                             strings_of_interest=['docx', 'doc'],
                                             identifier='docx',
                                             print_interim=print_interim)
        self.doc_links.update(docx_links)

        # PDFs
        pdf_links = get_doc_links_from_href(url=url,
                                            strings_of_interest=['.pdf'],
                                            identifier='pdf',
                                            kind='contains',
                                            print_interim=print_interim)

        self.doc_links.update(pdf_links)

        #  Google Docs
        google_links = get_doc_links_from_href(url=url,
                                               strings_of_interest=['drive.google', 'docs.google'],
                                               identifier='google',
                                               print_interim=print_interim,
                                               kind='contains')
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


class SecondLevelLinks:
    """This will be a class for the second level of districts and links"""

    def __init__(self, titles_urls):
        self.doc_links = {}
        self.crawl(titles_urls=titles_urls)
        self.docs_df = self.make_df()

    def make_df(self):
        docs_df = pd.DataFrame.from_dict(self.doc_links,
                                         orient='index',
                                         columns=['title', 'type'])
        docs_df = docs_df.reset_index()
        docs_df = docs_df.rename(columns={"index": "link"})
        docs_df = docs_df.set_index('title')

        return docs_df

    def crawl(self, titles_urls):
        for key, url in titles_urls.items():
            try:
                self._get_tricky_docs(url=url, title=key)
            except Exception as e:
                print("ERROR...", key, e)

    def _get_tricky_docs(self, url, title):
        # from not just hrefs, but scripts, and iframes

        docx_links = get_doc_links_from_href_scripts_iframes(url=url,
                                                             identifier='docx',
                                                             title=title,
                                                             strings_of_interest=['.doc', '.docx'],
                                                             kind='ending')
        self.doc_links.update(docx_links)

        pdf_links = get_doc_links_from_href_scripts_iframes(url=url,
                                                            identifier='pdf',
                                                            title=title,
                                                            strings_of_interest=['.pdf'],
                                                            kind='contains')
        self.doc_links.update(pdf_links)

        google_drive_links = get_doc_links_from_href_scripts_iframes(url=url,
                                                                     identifier='google',
                                                                     title=title,
                                                                     strings_of_interest=['drive.google',
                                                                                          '.docs.google'],
                                                                     kind='contains')
        self.doc_links.update(google_drive_links)
