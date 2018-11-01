from lxml.html.soupparser import convert_tree
from bs4 import SoupStrainer
import pandas as pd
from app.fund_search_helpers import *


def get_vals():
    # process command line args
    args = sys.argv[1:]
    largs = len(args)
    if largs < 1:
        print("You must enter at least one ticker symbol to use this program")
        sys.exit()
    if args > 1:
        for each in args:
            run_search(each)
    else:
        run_search(args[0])


def run_search(symbol):
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
        tsv = tab.to_csv(path_or_buf='/tmp/{}.tsv'.format(symbol), sep='\t')
        return tsv


if __name__ == "__main__":
    run_search('0001699622')
    # run_search('123')
    # run_search('{}')
