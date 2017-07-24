import json
import csv
from bs4 import BeautifulSoup as bs

# Filetype: csv
def parse(data, file):
    # Append file ext.
    fname = file
    ofile = open(fname, 'a')
    csv_file = csv.writer(ofile)
    # Header
    csv_file.writerow(["lat", "lng", "lodgeunitid", "html"])
    for entry in data:
        csv_file.writerow([entry["lat"], entry["lng"], entry["lodgeunitid"], entry["html"]])
    ofile.close()
    return fname