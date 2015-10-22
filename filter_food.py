import json
from utils import *

def filter_food(line):
	if 'categories' in line:
		cats = line['categories']
		return 'Food' in cats or 'Restaurants' in cats
	return False

def save_restaurants():
	data = load_data('yelp_academic_dataset_business.json', filter_food)
	f = open('food_businesses.json', 'w')
	for line in data:
		f.write(json.dumps(line) + '\n')
	f.close()

save_restaurants()
