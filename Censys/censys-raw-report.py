#!/usr/bin/python
# Pull report on if latest data dumps are ready

import sys
import json
import requests

API_URL = "https://www.censys.io/api/v1"
UID = "YOUR-UID"
SECRET = "YOUR-SECRET"

res = requests.get(API_URL + "/data", auth=(UID, SECRET), verify=False)
if res.status_code == 404:
    sys.exit("[ERROR] 404 - Not found")
elif res.status_code == 429:
    sys.exit("[ERROR] 429 - Rate Limit Exceeded")
elif res.status_code == 500:
    sys.exit("[ERROR] 500 - Internal Server Error")
elif res.status_code != 200:
    sys.exit("error occurred: %s" % res.json()["error"])
else:
    for name, series in res.json()["raw_series"].iteritems():
        print series["name"], "was last updated at", series["latest_result"]["timestamp"]
