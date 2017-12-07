#!/usr/bin/env python

import argparse
import json
import os
import requests
import sys
import datetime
from datetime import datetime
import dateutil
import dateutil.tz
import time

def getPVData(archurl, pvParams):
	url = archurl + '/retrieval/data/getData.txt'
	getPVDataResponse = requests.get(url, params=pvParams)

	return getPVDataResponse

def convertTimestamp(timestamp):
	ts = timestamp
	is_dst = time.daylight and time.localtime().tm_isdst > 0 
	current_tz = time.tzname[0] if is_dst else time.tzname[1]
	utc_offset = - (time.altzone if is_dst else time.timezone)
	ts = datetime.fromtimestamp(int(timestamp), dateutil.tz.tzoffset(current_tz, utc_offset)).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

	return ts

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='getPVData', description='takes in a list of PVs and a start and end time, then returns the data for those PVs over that time period')
	parser.add_argument("url", help="This is the URL to the appliance cluster. For example, http://arch-app.slac.stanford.edu")
	parser.add_argument("file", help="A CSV file with a list of PVs")
	parser.add_argument("--start", help="Start time to get data for PVs")
	parser.add_argument("--end", help="End time to get data for PVs")
	args = parser.parse_args()
	lines = []
	with open(args.file, 'r') as f:
	    lines = f.readlines()

	for line in lines:
		line = line.strip()
		parts = line.split(",")
		if len(parts) != 1:
			print "Invalid PV, skipping {}".format(line)
			continue
		pv = parts[0].strip()
		starttime = convertTimestamp(args.start)
		endtime = convertTimestamp(args.end)
		pvParams = (("pv", pv), ("from", starttime), ("to", endtime))
		getPVDataResponse = getPVData(args.url, pvParams)
		if getPVDataResponse.status_code != requests.codes.ok:
			print "{} returned status code {} retrieving data for {}".format(parser.prog, getPVDataResponse.status_code, pv)
		else:
			print getPVDataResponse.text
		time.sleep(1.0)
