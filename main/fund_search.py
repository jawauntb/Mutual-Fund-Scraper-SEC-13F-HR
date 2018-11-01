from fund_search_helpers.fund_search_helpers import run_search
import sys


def query():
    # process command line args
    args = sys.argv[1:]
    largs = len(args)
    if largs < 1:
        print("You must enter at least one ticker symbol to use this program")
        sys.exit()
    if largs > 2:
        for each in args:
            run_search(each)
    else:
        run_search(args[0])


if __name__ == "__main__":
    # run_search('0001699622')
    # run_search('0001166559')
    # run_search('0001039807')
    # run_search('0001393389')
    # run_search('0001730511')
    # run_search('0001665633')
    query()

