import json
from utils import *

def filter_by_city(data, city):
	def city_filter(line):
		if 'city' in line:
			return city in line['city']
		return False
	return filter(city_filter, data)

def map_to_arg(data, arg):
	return [x[arg] for x in data]
