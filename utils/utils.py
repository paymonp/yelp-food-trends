import json 

def filter_none(line):
	return True

def load_data(fname, filter_func=filter_none):
	f = open(fname, 'r')
	rawdata = f.readlines()
	return filter(filter_func, map(json.loads, rawdata))