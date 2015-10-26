#!/usr/bin/python
# Fetch the raw SSL/TLS Certificate from the CIRC.lu database

# Usage: ./fetch-cert.py.dist -q c46fed822dadac3f31f9bb4d1a78a1d9eae4567b
# Output: JSON

import argparse
import sys
import json
try:
    import requests
except:
    sys.exit("[ERROR] Python Requests library required")


# Edit as required
AUTH_USER = "YOUR_USER"
AUTH_PASS = "YOUR_PASSWORD"


def query_api(QUERY, OUTPUT):
    """Query the SSL API"""
    print "Query: " + str(QUERY)
    API_URL = "https://www.circl.lu/v2pssl/cfetch/" + str(QUERY)
    req = requests.get(API_URL, auth=(AUTH_USER, AUTH_PASS))
    if req.status_code == 200:
        print "Writing output: ",
        data = req.json()
        if OUTPUT is None:
            QUERYT = QUERY + ".json"
            print QUERYT
            with open(QUERYT, 'w') as fh:
                json.dump(data, fh)
        else:
            print OUTPUT
            with open(OUTPUT, 'w') as fh:
                json.dump(data, fh)
    else:
        sys.exit("[ERROR] Code: %s" % req.status_code)


def __main__():
    """Get this party started"""
    parser = argparse.ArgumentParser(description='DESCRIPTION HERE')
    parser.add_argument('--query', '-q', dest='query', help='Query to run')
    parser.add_argument('--output', '-o', dest='output', help='Save output to file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    QUERY = args.query
    OUTPUT = args.output

    if not args.query:
        sys.exit(parser.print_help())
    else:
        query_api(QUERY, OUTPUT)


if __name__ == '__main__':
    __main__()
