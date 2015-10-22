from sklearn import linear_model
from sklearn.cross_validation import KFold

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

crossvalidate(X, y)
