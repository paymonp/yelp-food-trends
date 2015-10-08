import json
import utils

def filter_food(line):
	if 'categories' in line:
		cats = line['categories']
		return 'Food' in cats or 'Restaurants' in cats
	return False

def save_restaurants():
	data = load_data('yelp_academic_dataset_business.json', filter_food)
	f = open('food_businesses.json')
	for line in data:
		f.write(line)

save_restaurants()
	