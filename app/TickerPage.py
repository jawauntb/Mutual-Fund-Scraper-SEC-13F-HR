from app.fund_search_helpers import get_response_from_ticker, set_url
from lxml import html


class TickerPage(object):

    def __init__(self, ticker):
        self.ticker = ticker
        self.url = set_url(ticker)
        self.page = get_response_from_ticker(ticker)
        self.status = self.page.status_code
        self.tree = html.fromstring(self.page.content)

    def xpath_exists(self, xpath):
        tree = self.tree
        if tree.xpath(xpath):
            return True
        else:
            return False

    def page_is_valid(self):
        invalid = '//*[@id="contentDiv"]/div[@class="noCompanyMatch"]'
        correct = '//*[@id="contentDiv"]/div[1]/div[3]/span[@class="companyName"]/a'
        no_match = '/html/body/div/center/h1[contains(., "No matching CIK.")]'
        if self.xpath_exists(correct):
            print('you have entered a valid url, which is {}'.format(self.url))
            return True
        else:
            if self.xpath_exists(no_match):
                print('EDGAR does not have a page that matches the values you entered, please try again')
            if self.xpath_exists(invalid):
                print('You have entered an invalid or empty ticker, there is no page for the value')
            return False

    def get_value_at_xpath(self, xpath):
        if self.xpath_exists(xpath):
            value = self.tree.xpath(xpath)
            return value
        else:
            wrong = 'The xpath you provided does not exist on this page'
            return wrong

    def find_table_contents(self):
        filings_table = '//*[@id="seriesDiv"]/table/tbody'
        if self.xpath_exists(filings_table):
            print("yes")
            table = self.get_value_at_xpath(filings_table)


if __name__ == "__main__":
    t = TickerPage('0001166559')
    print(t.url)
    t.find_table_contents()
    for each in t.tree.body:
        print(each)
