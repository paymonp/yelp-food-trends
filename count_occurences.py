import json
import datetime
import sys
from utils import *

#businesses = load_data("yelp_academic_dataset_business.json")
#checkins = load_data("yelp_academic_dataset_checkin.json")
#reviews = load_data("yelp_academic_dataset_review.json")
#users = load_data("yelp_academic_dataset_user.json")
#tips = load_data("yelp_academic_dataset_tip.json")



def in_time_range(timestamp, timerange):
	date_start, date_end = None, None
	timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d")

	if timerange[0]:
		date_start = datetime.datetime.strptime(timerange[0], "%Y-%m-%d")

	if timerange[1]:
		date_end = datetime.datetime.strptime(timerange[1], "%Y-%m-%d")

	if date_start and timestamp < date_start:
		return False

	if date_end and timestamp > date_end:
		return False

	return True



def count_occurrences(query, reviews, time_start=None, time_end=None, business_ids=None):
	date_counts = {}
	for r in reviews:
		text = r['text']
		date = r['date']
		converted_date = datetime.datetime.strptime(date, "%Y-%m-%d")
		
		time_constraint_valid = in_time_range(date, (time_start, time_end))
		location_constraint_valid = not business_ids or (r['business_id'] in business_ids)
		if time_constraint_valid and location_constraint_valid:
			for q in query:
				if q in text:
					key = (converted_date.month, converted_date.year)
					if key in date_counts:
						date_counts[key] += 1
					else:
						date_counts[key] = 1
	return date_counts


if len(sys.argv) > 1:
	reviews = load_data("review_test.json")
	query = sys.argv[1].strip().split(',')
	count_occurrences(query, reviews)

	date_counts = count_occurrences(query, reviews)
	print(sorted(date_counts.items(), key=lambda x: x[1], reverse=True)[0:10])
