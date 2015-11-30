# selective_featurize(picks)
# picks:    list of keys from the business json to consider
# returns:  tuple ([list of ratings], [list of feature vectors])
#
# example usage to include all features:
#   selective_featurize(['attributes', 'count', 'price', 'hours'])
# or try python selective_model.py

import json

# stupid stuff to import from a parent dir because python packaging isn't working for me
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir + '/utils')

import env


_MINUTES_AVG = 84 * 60

def selective_featurize(picks, path=env.SAMPLE_PATH):
  # everything returns an int except :attributes
  hashers = {
    'attributes': attributes_hash,
    'count': lambda d: d['review_count'],
    'price': lambda d: d['attributes']['Price Range'] if 'Price Range' in d['attributes'] else 0,
    'hours': hours_hash
  }
  training_data = []
  labels = []

  # sanity check
  for p in picks:
    if p not in hashers:
      print 'Invalid argument to feature selector: must be out of: ', hashers.keys()
      return

  with open(path, 'r') as input:
    for line in input:
      biz = json.loads(line)
      vec = []

      for key in picks:
        result = hashers[key](biz)
        # stupid
        if not isinstance(result, list):
          result = [result]
        vec.extend(result)

      training_data.append(vec)
      labels.append(biz['stars'])

  return labels, training_data

# return number of minutes open per week
def hours_hash(d):
  hours = d['hours']
  if len(hours) > 0:
    total = 0
    for day in hours:
      start, end = hours[day]['open'], hours[day]['close']
      start_h, start_m = int(start[:2]), int(start[3:5])
      end_h, end_m = int(end[:2]), int(end[3:5])

      h_diff = end_h - start_h
      m_diff = end_m - start_m
      # negative difference means the closing times goes until the next day, so we take the complement of the 24 hour day
      # total difference of 0 means open 24 hour I guess
      if h_diff < 0 or h_diff == 0 and m_diff == 0:
        h_diff = 24 + h_diff

      # negative minutes play out nicely
      total += h_diff * 60 + m_diff 
    return total
  else:
    return _MINUTES_AVG

# 0: false, 1: true, 2: N/A
def attributes_hash(d):
  attrs = d['attributes']
  vec = []
  # free to change this
  for key in ['Take-out', 'Accepts Credit Cards', 'Drive-Thru', 'Outdoor Seating', 'Delivery', 'Has TV', 'Takes Reservations', 'Good for Kids', 'Good For Groups']:
    if key in attrs:
      vec.append(int(attrs[key] == True))
    else:
      vec.append(2)
  return vec

def main():
  print selective_featurize(['attributes', 'count', 'price', 'hours'])

if __name__ == "__main__":
  main()

