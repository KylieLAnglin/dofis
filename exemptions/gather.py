# Imports
import urllib
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin


# Functions

def get_doc_links_from_href(soup, strings_of_interest, identifier, get_title=True, title='', print_interim=True,
                            kind='ending'):
    """
    First level links

    Takes soup and extracts hrefs of interest and titles them.
    :param soup: From BeautifulSoup
    :param strings_of_interest: what strings are you looking for inside the href?
    :param identifier: how do you identify these types
    :param get_title: get title or provide title? False = provide title.
    :param title: if providing title, what is it
    :param print_interim: want to print interim output?
    :param kind: -- The kind of href we're trying to detect (default: 'ending', alternative 'containing')
    :return:
    """
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


def get_doc_links_from_url(url, identifier, title, strings_of_interest, kind):
    """
    Second level links
    :param url:
    :param identifier:
    :param title:
    :param strings_of_interest:
    :param kind:
    :return:
    """
    retrieved_links = {}
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read()
        sopa = BeautifulSoup(html)
        for link in sopa.find_all('a'):  # TODO create clean link function
            current_link = link.get('href')
            current_link = clean_link(url= url, current_link = current_link)
            condition_mapping = {
                'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                'contains': [strng in current_link for strng in strings_of_interest],
            }
            condition = condition_mapping[kind]
            if any(condition):
                retrieved_links[current_link] = (title, identifier)
        # TODO <- Figure out how to gracefully handle iframes without src attributes
        for iframe in sopa.find_all('iframe'):
            current_link = iframe.attrs['src']
            current_link = clean_link(url= url, current_link = current_link)
            condition_mapping = {
                'ending': [current_link.endswith(ending) for ending in strings_of_interest],
                'contains': [strng in current_link for strng in strings_of_interest],
            }
            condition = condition_mapping[kind]
            if any(condition):
                retrieved_links[current_link] = (title, identifier)
        for script in sopa.find_all('script'):
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


# df = pd.DataFrame.from_dict(retrieved_links, orient='index', columns=['title', 'type'])
#    df2 = df.reset_index()
#   retrieved_links_df = df2.set_index('title')
#  retrieved_links_df = retrieved_links_df.rename(columns={"index": "link"})


###
#   Classes
###
class FirstLevelLinks:
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
        docx_links = get_doc_links_from_href(soup=self.soup,
                                             strings_of_interest=['docx', 'doc'],
                                             identifier='docx',
                                             print_interim=print_interim)
        self.doc_links.update(docx_links)

        # PDFs
        pdf_links = get_doc_links_from_href(soup=self.soup,
                                            strings_of_interest=['.pdf'],
                                            identifier='pdf',
                                            kind='contains',
                                            print_interim=print_interim)

        self.doc_links.update(pdf_links)

        #  Google Docs
        google_links = get_doc_links_from_href(self.soup,
                                               strings_of_interest=['drive.google'],
                                               identifier='google',
                                               print_interim=print_interim,
                                               kind='contains')
        self.doc_links.update(google_links)

        #  Google Docs
        google_links = get_doc_links_from_href(self.soup,
                                               strings_of_interest=['docs.google'],
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
    """This will be a class for the first level of districts and links"""

    def __init__(self, titles_urls):
        self.doc_links = {}
        self.crawl(titles_urls=titles_urls)


    def crawl(self, titles_urls):
        for key, url in titles_urls.items():
            try:
                self._get_tricky_docs(url=url, title=key)
            except Exception as e:
                print("ERROR...", key, e)

    def _get_tricky_docs(self, url, title):
        # Word Docs

        docx_links = get_doc_links_from_url(url=url,
                                            identifier='docx',
                                            title=title,
                                            strings_of_interest=['.doc', '.docx'],
                                            kind='ending')
        self.doc_links.update(docx_links)

        pdf_links = get_doc_links_from_url(url=url,
                                           identifier='pdf',
                                           title=title,
                                           strings_of_interest=['.pdf'],
                                           kind='contains')
        self.doc_links.update(pdf_links)

        google_drive_links = get_doc_links_from_url(url=url,
                                                    identifier='google',
                                                    title=title,
                                                    strings_of_interest=['drive.google', '.docs.google'],
                                                    kind='contains')
        self.doc_links.update(google_drive_links)
