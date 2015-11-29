from env import *
import random
import linecache
import json


# wc -l yelp_academic_dataset_business.json
_BUSINESS_LINES = 61184
# number of samples
_LIMIT = 10000

def main():
  # construct full random ordering of indices. 0 is invalid idx
  indices = random.sample(range(1, _BUSINESS_LINES), _BUSINESS_LINES - 1)
  random_idx = 0;

  in_path = DATASET_PATH + 'yelp_academic_dataset_business.json'
  out_file = open(OUTPUT_PATH + 'sample.txt', 'w')

  for i in range(_LIMIT):
    line_dict = json.loads(linecache.getline(in_path, indices[random_idx]))

    if 'categories' in line_dict and 'Restaurants' in line_dict['categories']:
      out_file.write(json.dumps(line_dict) + '\n')
    else:
      # while the next line isn't a restaurat, go to the next sampled index
      while 'categories' not in line_dict or 'categories' in line_dict and 'Restaurants' not in line_dict['categories']:
        random_idx += 1
        line_dict = json.loads(linecache.getline(in_path, indices[random_idx]))
      out_file.write(json.dumps(line_dict) + '\n')

    random_idx += 1

  out_file.close()

if __name__ == "__main__":
  main()