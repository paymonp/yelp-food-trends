import json
import datetime
import sys

def filter_none():
	return True

def load_data(fname):
	f = open(fname, 'r')
	data = []
	rawdata = f.readlines()
	for line in rawdata:
		data.append(json.loads(line))
	f.close()
	return data

