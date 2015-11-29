import json
from utils import load_data
import food_lib
import env

def filter_reviews():
	businesses = load_data("food_businesses.json")
	business_ids = set(food_lib.map_to_arg(food_lib.filter_by_city(businesses, "Las Vegas"), "business_id"))
	out_file = open('vegas_reviews.json', 'w+')
	with open(env.DATASET_PATH + 'yelp_academic_dataset_review.json', 'r') as f:
		for line in f:
			line_json = json.loads(line)
			if line_json['business_id'] in business_ids:
				out_file.write(json.dumps(line_json) + '\n')



def process_categories():
	reviews = load_data("vegas_reviews.json")
	def pizza(line):
		return 'Pizza' in line['categories']
	vegas_cats = set(food_lib.map_to_arg(load_data("food_businesses.json", pizza), 'business_id'))
	times = []
	for r in reviews:
		if r['business_id'] in vegas_cats:
			times.append(r['date'])
	print(sorted(times))


# process_categories()

filter_reviews()