import json
import csv

# Filetype: csv
def parse(data, file):
    # Append file ext.
    fname = file
    ofile = open(fname, 'w')
    csv_file = csv.writer(ofile)
    # Header
    csv_file.writerow(["lat", "lng", "lodgeunitid", "html"])
    for entry in data:
        csv_file.writerow([entry["lat"], entry["lng"], entry["lodgeunitid"], entry["html"]])
    ofile.close()
    return fname