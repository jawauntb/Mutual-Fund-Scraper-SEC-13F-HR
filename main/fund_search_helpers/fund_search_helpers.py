import requests
from time import sleep
import sys
from bs4 import BeautifulSoup
import pandas as pd


def set_url(ticker):
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany'.format(str(ticker))
    return url


def get_url_response_code(url):
    req = requests.get(url)
    status = req.status_code
    return status
    # tree = html.fromstring(req.content)


def url_is_valid(url):
    if get_url_response_code(url) == 200:
        return True
    else:
        print('the url you entered is not valid')
        print('the response from the request was {}'.format(get_url_response_code(url)))
        return False


def get_url(url):
    if url_is_valid(url):
        response = requests.get(url)
        sleep(0.00005)
        return response
    else:
        print('The URL you are trying to use is not valid, please enter a valid url')
        return get_url_response_code(url)


def get_response_from_ticker(ticker):
    url = set_url(ticker)
    response_page = get_url(url)
    print('navigating to url {}'.format(url))
    return response_page


def get_headers(table):
    heads = table.find_all('th')
    headers = []
    for head in heads:
        h = head.text
        headers.append(h)
    return headers


def get_table_contents(table):
    data = []
    headers = get_headers(table)
    head_len = len(headers)
    content = (table.find_all('tr'))[1:]
    for row in content:
        cols = row.find_all('td')
        r = {}
        for i in range(head_len):
            col = cols[i]
            if col.find('a'):
                col = col.a['href']
                r[headers[i]] = col
            else:
                r[headers[i]] = col.text
            data.append(r)
    return data


# returns the table containing desired data
def get_table(soup, attr):
    if soup is not None:
        print('constructing table')
        table = soup.find("table", attrs=attr)
        tab_l = get_table_contents(table)
        return tab_l
    else:
        sys.exit()


# creates the full url of the selected path and opens the page
def get_page_at_path(path):
    root = 'https://www.sec.gov'
    full_url = root + path
    page = requests.get(full_url)
    return page


# checks if the document should be clicked because it is a 13f
def document_is_correct(document_row):
    if document_row["Filings"] == '13F-HR':
        return True
    else:
        print('there are no 13F filings here')
        return False


# returns the page containing the full 13f filing
def get_document_link(documents_table):
    dt_len = len(documents_table)
    i = 0
    while i < dt_len:
        if document_is_correct(documents_table[i]):
            link = documents_table[i]["Format"]
            print('the link to this table of filings is https://www.sec.gov{}'.format(link))
            return link
        elif i < (dt_len-1):
            i += 1
        else:
            if document_is_correct(documents_table[i]) is False:
                print('There are no 13-f files here')
                sys.exit()


# searches for the full 13f document in the table of documents at a selected document's path
def get_complete_thirteen_f(path):
    page = get_page_at_path(path)
    soup = BeautifulSoup(page.content, "lxml")
    file_link = soup.find(text='INFORMATION TABLE').parent.parent.a['href']
    thirteen_f = get_page_at_path(file_link)
    print('retrieving raw 13F')
    return thirteen_f


def run_search(symbol):
    print('searching for 13F-HR forms related to CIK/Ticker {}'.format(symbol))
    page = get_response_from_ticker(symbol)
    soup = BeautifulSoup(page.content, "lxml")
    no_match = "No matching CIK."
    if (soup.find_all('div', attrs={"class": "noCompanyMatch"})) or (soup.find_all(string=no_match)):
        print('You have entered a value which does not exist.')
        sys.exit()
    else:
        print('Running search for filings related to {}'.format(symbol))
        table = get_table(soup, {'class': 'tableFile2'})
        thirteen_f_link = get_document_link(table)
        thirteen_f_soup = BeautifulSoup(get_complete_thirteen_f(thirteen_f_link).content, features="lxml")
        datatable = str((thirteen_f_soup.find_all('table')))
        df = pd.read_html(datatable)
        lim = len(df)
        tab = df[lim-1]
        pathto = '/tmp/{}.tsv'.format(symbol)
        tsv = tab.to_csv(path_or_buf=pathto, sep='\t')
        print('your file is at {}, please navigate to this path to view tsv file'.format(pathto))
        return tsv
