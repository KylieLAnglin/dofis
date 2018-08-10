from urllib import request

import requests
from tika import parser
import urllib.parse as parse
from interruptingcow import timeout
import ssl


def get_plain_text(link):
    """

    :param link: link to a document (including an HTML doc),
    :return: plain text of that document
    """
    print('Current link: {}'.format(link), end='\r')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    if 'drive.google.com' in link:
        try:
            link = convert_google_url(link)
        except Exception as e:
            print("Google Error:", e)
    try:
        with timeout(45, exception=RuntimeError):
            req = request.Request(link, headers=headers)
            buff = request.urlopen(req, context=ctx)
            parsed = parser.from_buffer(buff)
            return parsed['content']
            pass

    except Exception as e:
        try:
            resp = requests.get(link)
            parsed = parser.from_buffer(resp.content)
            return parsed['content']
        except:
            print('error:', e, 'link:', link)
            return 'UNAVAILABLE'


def convert_google_url(url):
    """
    Given a URL to a rendered Google Doc, convert it to a downloaded/downloadable Google Doc
    """
    parsed = parse.urlparse(url)
    doc_id_ind = parsed.path.split('/').index('d') + 1  # DocID follows /d in URL
    doc_id = parsed.path.split('/')[doc_id_ind]
    unparsed = parsed._replace(path='/uc?export=downloads&id=' + doc_id)
    return parse.urlunparse(unparsed)

def remove_whitespace(df, text_col):
    '''
    Remove all \n, \t, \r characters from raw text
    '''
    col = text_col
    clean_text = df[col].map(lambda x: ' '.join(x.split()))
    df = df.copy()
    df[col] = clean_text
    return df

def remove_nulls(df):
    '''
    Remove all records from text column that are None or UNAVAILABLE
    '''
    col = 'text'
    df = df.copy()
    df = df[(df[col] != 'UNAVAILABLE') & (df[col].notnull())]
    return df