import json
from utils import load_data
from food_lib import *

def featurize():
	def pizza(line):
		return 'Pizza' in line['categories']
	vegas_pizza = filter_by_city(load_data("food_businesses.json", pizza), 'Las Vegas')
	training_data = []
	labels = []
	for biz in vegas_pizza:
		el = []
		if 'Price Range' in biz['attributes']:
			el.append(biz['review_count'])
			el.append(biz['attributes']['Price Range'])
			training_data.append(el)
			labels.append(biz['stars'])
	return labels, training_data

labels, training_data = featurize()
