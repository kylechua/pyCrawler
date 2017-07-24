import json
import os

def parse(data, fname):
    a = list()
    if not os.path.isfile(fname):
        a.append(data)
        with open(fname, 'w') as ofile:
            ofile.write(json.dumps(a, indent=2))
    else:
        with open(fname) as feedsjson:
            feeds = json.load(feedsjson)
        feeds.append(data)
        with open(fname, 'w') as ofile:
            ofile.write(json.dumps(feeds, indent=2))