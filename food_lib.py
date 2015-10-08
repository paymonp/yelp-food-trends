import json
from utils import *

def filter_by_city(data, city):
	def city_filter(line):
		line = line.lower()
		if 'city' in line:
			return city in line['city']
		return False
	return filter(city_filter, data)

