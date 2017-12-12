#!/usr/bin/env python

import argparse
import json
import requests
import time

def getPVStatus(bplURL, pv):
	# retrieves the status for a given PV
	url = bplURL + '/getPVStatus'
	payload = { 'pv': pv }
	getPVStatusResponse = requests.post(url, params=payload)
	return getPVStatusResponse

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('url', help='This is the URL to the mgmt bpl interface of the archiver appliance cluster, e.g. http://archapp.slac.stanford.edu/mgmt/bpl')
	parser.add_argument('file', help='A file containing a list of PVs, one PV per line')
	args = parser.parse_args()
	pvList = []

	with open(args.file, 'r') as f:
		pvList = f.readlines()

	for pv in pvList:
		pv = pv.strip()
	
		pvStatusResponse = getPVStatus(args.url, pv)
		if pvStatusResponse.status_code != requests.codes.ok:
			print "returned status code {} retrieving data for {}".format(pvStatusResponse.status_code, pv)
		else:
			parsedResponse = json.loads(pvStatusResponse.text)
			print json.dumps(parsedResponse, indent=4, separators=(',', ': '))
		
		time.sleep(1.0)
