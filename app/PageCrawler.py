# filings_table = '//*[@id="seriesDiv"]/table/tbody'
# proper_filing =//*[@id="seriesDiv"]/table/tbody/tr[2]/td[contains(., "13F-HR")]
# report_at_date = '//*[@id="seriesDiv"]/table/tbody/tr[2]/td[contains(., {})]'.format(datestring)

def get_most_recent_report():
    pass


def get_report_near_date(year_num, month_num, day_num):
    if year_num > 2050 or month_num > 12 or day_num > 31:
        print("the date you entered is invalid, please enter a valid date")
    else:
        datestring = str(year_num) + '-' + str(month_num) + '-' + str(day_num)
        # once a quarter release, check first value, if not true then check next