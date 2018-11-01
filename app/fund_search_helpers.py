import requests
import re
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


def get_table(soup, attr):
    if soup is not None:
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
        return False


# returns the page containing the full 13f filing
def get_document_link(documents_table):
    dt_len = len(documents_table)
    i = 0
    while i < dt_len:
        if document_is_correct(documents_table[i]):
            link = documents_table[i]["Format"]
            print('the link is {}'.format(link))
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
    file_link = soup.find(text='DESCRIPTION FOR INFORMATION TABLE').parent.parent.a['href']
    thirteen_f = get_page_at_path(file_link)
    return thirteen_f

