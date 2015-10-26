#!/usr/bin/python
# Script to query the Censys.io API for websites, IPv4 addresses
# and SSL/TLS certificates

# Usage: censys-query.py -i 192.168.0.1 (output written to 192.168.0.1.json)
# Usage: censys-query.py -w cisco.com -o cisco-results.json
# Usage: censys-query.py -c 750cb36078bc8b9387397bc9ac0f6515a740a3be0210c01c2ba1501cb11ed703

import argparse
import json
import sys
try:
    import requests
except:
    sys.exit("[ERROR] Python Requests library required")

# Update as required
UID = "YOUR_UID"
SECRET = "YOUR_SECRET"


def check_status(http_status_code):
    """Return our HTTP status action"""
    if http_status_code == 404:
        sys.exit("[ERROR] 404 - Data not found")
    elif http_status_code == 429:
        sys.exit("[ERROR] 429 - Rate Limit Exceeded")
    elif http_status_code == 400:
        sys.exit("[ERROR] 400 - Bad Request")
    elif http_status_code == 500:
        sys.exit("[ERROR] 500 - Internal Server Error")
    elif http_status_code == 405:
        sys.exit("[ERROR] Something has gone horribly wrong !!")
    elif http_status_code == 200:
        print "200"


def get_api_url(QUERYTYPE):
    """Get the correct API URL"""
    BASE_URL = "https://www.censys.io/api/v1/view/"

    if QUERYTYPE == "ipv4":
        API_URL = BASE_URL + "ipv4/"
    elif QUERYTYPE == "websites":
        API_URL = BASE_URL + "websites/"
    elif QUERYTYPE == "certificates":
        API_URL = BASE_URL + "certificates/"

    return API_URL


def query_api(QUERYTYPE, QUERYSTRING, OUTPUT):
    """Query the Censys.io API"""

    API_URL = get_api_url(QUERYTYPE)
    FULL_URL = API_URL + QUERYSTRING
    print "Querying API...",
    res = requests.get(FULL_URL, auth=(UID, SECRET), verify=True)
    check_status(res.status_code)
    data = res.json()
    print "Writing output to file: ",
    if OUTPUT is None:
        OUTPUT = QUERYSTRING + ".json"
        print OUTPUT
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)
    else:
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='Censys API Query Tool')
    parser.add_argument('--query-website', '-w', dest='querywebsite', action="store_true", help='Query Censys for website data')
    parser.add_argument('--query-ipv4', '-i', dest='queryipv4', action="store_true", help='Query Censys for IPv4 data')
    parser.add_argument('--query-certificate', '-c', dest='querycert', action="store_true", help='Query Censys for certificate data')
    parser.add_argument('querystring', metavar='QUERY', help='Query string')
    parser.add_argument('--output', '-o', dest='output', help='Write output to file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    QUERYSTRING = args.querystring
    OUTPUT = args.output

    if args.queryipv4:
        QUERYTYPE = "ipv4"
        query_api(QUERYTYPE, QUERYSTRING, OUTPUT)
    elif args.querywebsite:
        QUERYTYPE = "websites"
        query_api(QUERYTYPE, QUERYSTRING, OUTPUT)
    elif args.querycert:
        QUERYTYPE = "certificates"
        if len(QUERYSTRING) < 64:
            sys.exit("[ERROR] We need a SHA256 hash.")
        else:
            query_api(QUERYTYPE, QUERYSTRING, OUTPUT)
    else:
        sys.exit(parser.print_help())


if __name__ == '__main__':
    __main__()
