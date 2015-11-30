import json
#from utils import load_data
#from food_lib import *
from sklearn import linear_model
from sklearn.cross_validation import KFold
import numpy as np 
from selective_model import selective_featurize
import glob



def half_int_round(a):
	#print(a)
	buckets = [int(a), int(a)+0.5, int(a)+1]
	best_dist = float('inf')
	best_bucket = None
	for b in buckets:
		if abs(a-b) < best_dist:
			best_dist = abs(a-b)
			best_bucket = b
	return best_bucket

def eval_model(pred, test):
	diff = pred-test
	#print(diff)
	diff[diff > 0.5] = 0
	diff[diff < -0.5] = 0
	diff[diff != 0] = 1
	return np.sum(diff) / float(pred.shape[0])


"""
def crossvalidate(X, y):

	print("NUM FEATURES", len(features))
	print("NUM FEATURES IN DATA MATRIX", X.shape[1])

	kf = KFold(X.shape[0], n_folds=10)
	mse_scores = []
	acc_scores = []
	for train, test in kf:
		Xtrain, ytrain = X[train], y[train]
		Xtest, ytest = X[test], y[test]
		#model = linreg(Xtrain, ytrain)
		#model = logreg(Xtrain, ytrain)
		model = lasso(Xtrain, ytrain)
		pred = model.predict(Xtest)
		pred = np.reshape(pred, (pred.shape[0], 1))
		pred = np.apply_along_axis(half_int_round, axis=1, arr=pred)
		mse = np.sum(np.multiply(pred-ytest, pred-ytest))
		mse_scores.append(mse)
		acc_scores.append(eval_model(pred, ytest))


	print(sum(acc_scores)/float(len(acc_scores)))
	print(sum(mse_scores)/float(len(mse_scores)))
"""

def linreg(X, y):
	model = linear_model.LinearRegression()
	model.fit(X, y)
	return model


def logreg(X, y):
	model = linear_model.LogisticRegression()
	model.fit(X, y)
	return model

def lasso(X, y):
	model = linear_model.Lasso()
	model.fit(X, y)
	return model

def score(X, labels, model):
	acc_scores = []
	pred = model.predict(X)
	pred = np.reshape(pred, (pred.shape[0], 1))
	pred = np.apply_along_axis(half_int_round, axis=1, arr=pred)
	acc_scores.append(eval_model(pred, labels))
	correct = sum(acc_scores)
	total = len(acc_scores)
	return correct, total

features = ['count', 'hours', 'Take-out', 'Accepts Credit Cards', 'Drive-Thru', 'Outdoor Seating', 'Delivery', 'Has TV', 'Takes Reservations', 'Good for Kids', 'Good For Groups']

def get_top_5_coef(model):
	coef = model.coef_
	indices = list(np.argsort(coef))
	print("High weights")
	for i in indices[-5:]:
		#print(i)
		print(features[i], coef[i])
	print('\n')
	
def get_bottom_5_coef(model):
	coef = model.coef_
	indices = list(np.argsort(coef))
	print("Low weights")
	for i in indices[0:5]:
		print(features[i], coef[i])
	print('\n')

# ... load data somewhow

def run_experiment():
	# EXP 1: Get geopgrahic specific classifiers
	files = glob.glob('training/divided/*.txt')
	models = {}

	for fname in files:
		# TODO: Write a regex to parse through the fname
		_, city = fname.split('/')[-1].split('-')
		labels, training_data = selective_featurize(['attributes', 'count', 'hours'], path=fname)
		labels = np.array(labels)
		training_data = np.array(training_data)
		model = linreg(training_data, labels)
		models[city] = model
		print(city)
		get_top_5_coef(model)
		get_bottom_5_coef(model)


	correct = 0.
	total = 0.

	files = glob.glob('validation/divided/*.txt')
	for fname in files:
		_, city = fname.split('/')[-1].split('-')
		labels, testing_data = selective_featurize(['attributes', 'count', 'hours'], path=fname)
		labels = np.array(labels)
		testing_data = np.array(testing_data)
		model = models[city]
		curr_correct, curr_total = score(testing_data, labels, model)
		correct += curr_correct
		total += curr_total
		print(city, curr_correct/float(curr_total))

	print("Geographically divided classifier accuracy: " + str(correct/total))


	#Exp 2: Get overall classifier
	fname = "training/sample.txt"
	labels, training_data = selective_featurize(['attributes', 'count', 'hours'], path=fname)
	labels = np.array(labels)
	training_data = np.array(training_data)
	model = linreg(training_data, labels)

	fname = "validation/sample.txt"
	labels, testing_data = selective_featurize(['attributes', 'count', 'hours'], path=fname)
	labels = np.array(labels)
	testing_data = np.array(testing_data)
	correct, total = score(testing_data, labels, model)
	print("Non-divided classifier accuracy: " + str(float(correct)/total))

run_experiment()




