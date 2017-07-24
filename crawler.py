import requests
import importlib
import copy
from time import sleep
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs

from package.config import *
from package.info import bcolors, getapiURL, getparser

# Parses the infile and returns a list of requests to try
def getrequestURLs(queryURL, infile):
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

def makeRequests(reqs, parser):
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
            parser.parse(data, OUTPUTFILE)
            print(bcolors.OKGREEN, "SUCCESS", bcolors.ENDC)
        except Exception as inst:
            print(bcolors.FAIL, "FAIL: No data found", bcolors.ENDC)
            # Could not parse data, do nothing
            pass

def main():
    # Open input file
    try:
        infile = open(INPUTFILE, 'r')
    except Exception as inst:
        print(bcolors.FAIL, inst, bcolors.ENDC)
        return

    # Parse input file
    source = infile.readline().replace('\n','')
    apiURL = getapiURL(source)
    reqs = getrequestURLs(apiURL, infile)
    
    # Fetch data from source, get the proper parser, and write to file
    parser = importlib.import_module(getparser(source))
    makeRequests(reqs, parser)

if __name__ == "__main__":
    main()
#print(url[1].split('.')[1])