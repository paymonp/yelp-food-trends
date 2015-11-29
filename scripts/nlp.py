import json
import sys
from textblob import TextBlob
import numpy as np

# Set up business-to-list-of-review-text map
raw_reviews = open("vegas_reviews.json", 'r+').readlines()

business_reviews = {}
failed = 0
total = 0
for raw_review in raw_reviews:
	try:
		review = json.loads(raw_review)
		business_id = review['business_id']
		if business_id in business_reviews:
			business_reviews[business_id].append(review['text'])
		else:
			business_reviews[business_id] = [review['text']]
	except Exception as e:
		failed += 1
		print(e)
	total += 1


print("failed", failed)
print("total", total)

# Set up business-to-min-max-mean-stddev map

review_stats_file = 'business_review_stats.json'

with open(review_stats_file, 'w') as fp:
	for i, id in enumerate(business_reviews.keys()):
		polarities = []

		if i % 100 == 0:
			sys.stdout.write('\r%0.5f%% - ' % (round((i + 0.0)/ total, 5)))
			sys.stdout.flush()

		for review_text in business_reviews[id]:
			polarities.append(TextBlob(review_text).sentiment.polarity)

		info = [len(polarities), np.min(polarities),np.max(polarities),np.mean(polarities), np.std(polarities)]

		fp.write(json.dumps({id: {'count': info[0], 'min': info[1], 'max': info[2], 'mean': info[3], 'std': info[4]}}) + '\n')

