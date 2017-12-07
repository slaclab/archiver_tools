#!/usr/bin/env python
'''Change archival parameters for PVs in a given list'''

import os
import sys
import argparse
import requests
import time
import urllib
import urllib2
import json
import datetime

def changeArchivalParameters(bplURL, pvParams):
	url = bplURL + '/changeArchivalParameters'
	resp = requests.get(url, params=pvParams)
	return resp.status_code
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("url", help="This is the URL to the mgmt bpl interface of the appliance cluster. For example, http://arch.slac.stanford.edu/mgmt/bpl")
	parser.add_argument("file", help="A CSV file, each line containing PV,samplingPeriod,samplingMethod")
	args = parser.parse_args()
	lines = []
	pvParamList = []
	pvParamKeys = ['pv', 'samplingperiod', 'samplingmethod']
	with open(args.file, 'r') as f:
		lines = f.readlines()
		for line in lines:
			pvParamVals = line.strip().split(',')
			pvParamDict = {key:value for (key, value) in zip(pvParamKeys, pvParamVals)}
			#pvParamList.append(pvParamDict)
			pvChangeParamsResponse = changeArchivalParameters(args.url, pvParamDict)
			print 'Response returned with status {}'.format(pvChangeParamsResponse)
			time.sleep(1.0)	
