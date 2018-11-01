import pytest
from main.fund_search_helpers.fund_search_helpers import *
# 'https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany'.format(ticker)
# test the following tickers/ciks: fctdx=0001364924 cmiex=0000773757, fzrox=0000035315,
# as well as: sehax=0000939934, fgmnx=0000751199, quasx= 0000081443, lmpmx=0000880366,  0001166559=


def test_set_url():
    ticker = 'abcdef'
    assert set_url(ticker) == 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=abcdef&owner=exclude&action=getcompany'


def test_get_url_response_code():
    ticker = set_url('fctdx')
    cik = set_url('0001364924')
    bad_tick = set_url('83979')
    useless_url = 'https://www.sec.gov/nvskjdhbv'
    assert get_url_response_code(ticker) == 200
    assert get_url_response_code(cik) == 200
    assert get_url_response_code(bad_tick) == 200
    assert get_url_response_code(useless_url) == 404


def test_url_is_valid():
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=fctdx&owner=exclude&action=getcompany'
    bad_url = 'https://www.sec.gov/hbfoajbeof'
    assert url_is_valid(url)
    assert url_is_valid(bad_url) is False


def test_get_url():
    url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=fctdx&owner=exclude&action=getcompany'
    assert get_url(url).status_code == 200


def test_get_response_from_ticker():
    ticker = 'cmiex'
    bad_ticker = 1
    assert get_response_from_ticker(ticker).status_code == 200
    assert get_response_from_ticker(bad_ticker).status_code == 200

###################################################################################################################
