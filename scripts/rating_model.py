import json
from utils import load_data
from food_lib import *
from sklearn import linear_model
from sklearn.cross_validation import KFold
import numpy as np 

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

labels = np.array(labels)
training_data = np.array(training_data)


print(training_data.shape, labels.shape)

def crossvalidate(X, y):
	kf = KFold(X.shape[0], n_folds=10)
	for train, test in kf:
		Xtrain, ytrain = X[train], y[train]
		Xtest, ytest = X[test], y[test]
		model = linreg(Xtrain, ytrain)
		score = model.score(Xtest, ytest)
		print(score)




def linreg(X, y):
	model = linear_model.LinearRegression()
	model.fit(X, y)
	return model



# ... load data somewhow

#crossvalidate(X, y)
