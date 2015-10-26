#!/usr/bin/python
# Script to query the Censys.io API for websites, IPv4 addresses
# and SSL/TLS certificates

# Usage: censys-query.py -i 192.168.0.1
# Usage: censys-query.py -w cisco.com -o cisco-results.json
# Usage: censys-query.py -c 750cb36078bc8b9387397bc9ac0f6515a740a3be0210c01c2ba1501cb11ed703 -o tm-cert.json

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


def query_cert(QUERYSTRING, OUTPUT):
    """Query Censys.io for a certificate"""
    API_URL = "https://www.censys.io/api/v1/search/certificates?"
    HTTP_DATA = {"query": "%s" % QUERYSTRING}
    print "Querying API...",
    res = requests.post(API_URL, auth=(UID, SECRET), data=json.dumps(HTTP_DATA), verify=True)
    check_status(res.status_code)
    data = res.json()
    matches = data["metadata"]["count"]
    if matches >= 1:
        print "Matches: " + str(matches)
    else:
        sys.exit("[INFO] No Matches Found :(")
    print "[INFO] Writing output to file"
    if OUTPUT is None:
        OUTPUT = QUERYSTRING + ".json"
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)
    else:
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)


def query_ipv4(QUERYSTRING, OUTPUT):
    """Query the API"""
    API_URL = "https://www.censys.io/api/v1/search/ipv4?"
    HTTP_DATA = {"query": "ip:%s" % QUERYSTRING}
    print "Querying API...",
    res = requests.post(API_URL, auth=(UID, SECRET), data=json.dumps(HTTP_DATA), verify=True)
    check_status(res.status_code)
    data = res.json()
    matches = data["metadata"]["count"]
    if matches >= 1:
        print "Matches: " + str(matches)
    else:
        sys.exit("[INFO] No Matches Found :(")
    print "[INFO] Writing output to file"
    if OUTPUT is None:
        OUTPUT = QUERYSTRING + ".json"
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)
    else:
        with open(OUTPUT, 'w') as output:
            json.dump(data, output)


def query_website(QUERYSTRING, OUTPUT):
    """Query the API"""
    API_URL = "https://www.censys.io/api/v1/search/websites?"
    HTTP_DATA = {"query": "%s" % QUERYSTRING}
    print "Querying API...",
    res = requests.post(API_URL, auth=(UID, SECRET), data=json.dumps(HTTP_DATA), verify=True)
    check_status(res.status_code)
    data = res.json()
    matches = data["metadata"]["count"]
    if matches >= 1:
        print "Matches: " + str(matches)
    else:
        sys.exit("[INFO] No Matches Found :(")
    print "[INFO] Writing output to file"
    if OUTPUT is None:
        OUTPUT = QUERYSTRING + ".json"
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

    if args.querywebsite:
        query_website(QUERYSTRING, OUTPUT)
    elif args.queryipv4:
        query_ipv4(QUERYSTRING, OUTPUT)
    elif args.querycert:
        query_cert(QUERYSTRING, OUTPUT)
    else:
        sys.exit("[ERROR] Query type required")

if __name__ == '__main__':
    __main__()
