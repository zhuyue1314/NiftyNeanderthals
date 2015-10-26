#!/usr/bin/python
# Script to query the Censys.io API for websites, IPv4 addresses
# and SSL/TLS certificates

# Usage: censys-query.py -t i -q 192.168.0.1 -o results.json
# Usage: censys-query.py -t w -q cisco.com -o cisco-results.json
# Usage: censys-query.py -t c -q 750cb36078bc8b9387397bc9ac0f6515a740a3be0210c01c2ba1501cb11ed703 -o tm-cert.json

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


def query_api(QUERYTYPE, QUERYSTRING, OUTPUT):
    """Query the API"""

    if QUERYTYPE == "w":
        QUERYTYPE = "websites"
    elif QUERYTYPE == "i":
        QUERYTYPE = "ipv4"
    elif QUERYTYPE == "c":
        QUERYTYPE = "certificates"
    else:
        sys.exit("[ERROR] Correct query type required")

    API_URL = "https://www.censys.io/api/v1/view/" + str(QUERYTYPE) + "/" + str(QUERYSTRING)
    print "Querying API..."
    res = requests.get(API_URL, auth=(UID, SECRET), verify=False)
    if res.status_code == 404:
        sys.exit("[ERROR] 404 - Not found")
    elif res.status_code == 429:
        sys.exit("[ERROR] 429 - Rate Limit Exceeded")
    elif res.status_code == 500:
        sys.exit("[ERROR] 500 - Internal Server Error")
    elif res.status_code != 200:
        sys.exit("error occurred: %s" % res.json()["error"])
    else:
        data = res.json()
        print "Writing output to file"
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
    parser.add_argument('--query-type', '-t', dest='querytype', help='[w]ebsite/[i]pv4/[c]ertificate')
    parser.add_argument('--query-string', '-q', dest='querystring', help='Query string')
    parser.add_argument('--output', '-o', dest='output', help='Write output to file')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    QUERYTYPE = args.querytype
    QUERYSTRING = args.querystring
    OUTPUT = args.output

    if not (args.querytype and args.querystring):
        sys.exit(parser.print_help())
    else:
        query_api(QUERYTYPE, QUERYSTRING, OUTPUT)


if __name__ == '__main__':
    __main__()
