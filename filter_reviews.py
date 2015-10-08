import json
from utils import load_data
import food_lib

businesses = load_data("food_businesses.json")
business_ids = set(food_lib.map_to_arg(food_lib.filter_by_city(businesses, "Las Vegas"), "business_id"))

print("ok so starting loading")
city = "Las Vegas"
relevant_reviews = []
#reviews = load_data("yelp_academic_dataset_review.json")

def filter_reviews():
	out_file = open('vegas_reviews.json', 'w+')
	with open('yelp_academic_dataset_review.json', 'r') as f:
		for line in f:
			line_json = json.loads(line)
			if line_json['business_id'] in business_ids:
				out_file.write(json.dumps(line_json) + '\n')
filter_reviews()
'''



print("loaded reviews.")
c = 0
for r in reviews:
	if r['business_id'] in business_ids:
		reviews.append(json.dumps(r))
	c += 1
	if c % 10 == 0:
		print('finished another 100000...')
		print(len(reviews)-c, 'left to go')

f = open("vegas_reviews.json", "w+")
for r in reviews:
	f.write(r) + "\n"
f.close()
'''