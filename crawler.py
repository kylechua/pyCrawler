import requests
import asyncio
import copy
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs
from time import sleep

inputURL = './data/in/input.txt'
RQDELAY = 2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Returns the base query URL for the given source
def getQueryURL(source):
    if source == 'xiaozhu':
        return 'http://www.xiaozhu.com/ajax.php?op=Ajax_GetDatas4Map&partner=&startDate=&endDate=&city=&putkey=&district=&landmark=&housetyperoomcnt=&facilities=&leasetype=&guestnum=&lowprice=&highprice=&pageno=&sort=&_='
    else: # Assume source given is already base query URL
        return source

# Parses the infile and returns a list of requests to try
def getRequestURLs(queryURL, infile):
    urlparts = urlsplit(queryURL)
    defaultKeys = parse_qs(urlparts.query, True)

    reqs = list()

    for line in infile:
        currentURL = list(urlparts)
        params = line.replace('\n','').split(',')
        queries = copy.deepcopy(defaultKeys)

        # Appropriate syntax for urlencode (e.g. 'city=5' becomes key-value pair ('city', '5'))
        for p in params:
            temp = p.split('=')
            key = temp[0]
            val = temp[1]
            # If key is a support query key, update it with val
            if key in defaultKeys:
                queries[key] = val

        # Remove list syntax for queries with only one element
        for key in queries:
            if isinstance(queries[key], list):
                if len(queries[key]) == 1:
                    queries[key] = queries[key][0]

        # Encode URL
        currentURL[3] = urlencode(queries)
        reqs.append((params, urlunsplit(currentURL)))

    return reqs

def makeRequests(reqs):
    count = 0
    total = len(reqs)
    for req in reqs:
        count += 1
        sleep(RQDELAY)
        # Get request
        try:
            print(bcolors.HEADER, "[", count, "of", total, "]", req[0], bcolors.ENDC, end="...", flush=True)
            result = requests.get(req[1])
            if result.status_code != 200:
                print(bcolors.FAIL, "FAIL:", result.status_code, "error", bcolors.ENDC)
                continue
        except Exception as inst:
            print(bcolors.FAIL, "FAIL:", inst, bcolors.ENDC)
            # Could not resolve request, move onto the next one
            continue
        # Parse JSON data
        try:
            data = result.json()
            print(bcolors.OKGREEN, "SUCCESS", bcolors.ENDC)
            # Call some func to parse data
        except Exception as inst:
            print(bcolors.FAIL, "FAIL: No data found", bcolors.ENDC)
            # Could not parse data, do nothing
            pass

def main():
    # Open input file
    try:
        infile = open(inputURL, 'r')
    except Exception as inst:
        print(bcolors.FAIL, inst, bcolors.ENDC)
        return

    # Parse input file
    source = infile.readline().replace('\n','')
    queryURL = getQueryURL(source)
    reqs = getRequestURLs(queryURL, infile)
    
    # Fetch data from source and parse to file
    makeRequests(reqs)

if __name__ == "__main__":
    main()
#print(url[1].split('.')[1])