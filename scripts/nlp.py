import json


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




