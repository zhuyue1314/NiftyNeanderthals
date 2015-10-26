#!/usr/bin/python
# Google API Query

import argparse
import sys
import json
try:
    import requests
except:
    sys.exit("[ERROR] Python Requests library required")


# Edit as required
GOOGLE_UID = "ADD_CSE_UID"
GOOGLE_CSE = "ADD_CSE"
GOOGLE_API_KEY = "ADD_API_KEY"
# Google Custom Search URL
GOOGLE_URL = "https://www.googleapis.com/customsearch/v1?key=" + GOOGLE_API_KEY + "&cx=" + GOOGLE_UID + ":" + GOOGLE_CSE + "&q="


def run_query(QUERY, OUTPUT):
    """Query our Google Custom Search Engine"""
    print "Search query: " + QUERY
    QUERY_URL = GOOGLE_URL + QUERY
    req = requests.get(QUERY_URL)
    if req.status_code == 200:
        print "[OK] ...",
        jsondata = req.json()
        with open(OUTPUT, 'w') as fh:
            print "Writing output"
            json.dump(jsondata, fh)
    else:
        sys.exit("[ERROR] Status Code: %s" % str(req.status_code))


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='DESCRIPTION HERE')
    parser.add_argument('--query', '-q', dest='query', help='Query to run')
    parser.add_argument('--output', '-o', dest='output', default='output.json', help='Write output to file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    QUERY = args.query
    OUTPUT = args.output

    if not args.query:
        sys.exit(parser.print_help())
    else:
        run_query(QUERY, OUTPUT)


if __name__ == '__main__':
    __main__()
