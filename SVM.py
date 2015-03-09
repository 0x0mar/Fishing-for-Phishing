import os
import sys, traceback
import re
import json
import lxml, MySQLdb
import lxml.html
from lxml.html.clean import Cleaner
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import numpy as np
from _ast import Break
import pickle


def classifySVM(n, db):
	i = 0
	allCopy = []
	cursor = db.cursor()
	
	#store n spam samples, randomly selected from the db
	execString = ("SELECT Content FROM Content ORDER BY RAND() LIMIT %s;"%n) 
	cursor.execute(execString)
	spamCopy = cursor.fetchall()
	#store n non-spam samples, randomly selected from the db
	execString = ("SELECT Content FROM safeContent ORDER BY RAND() LIMIT %s;"%n) 
	cursor.execute(execString)
	notSpamCopy = cursor.fetchall()
	
	lengths = []
	#put the copy in a vector and calculate lengths of the samples
	for row in spamCopy:
		allCopy.append(row[0])
		lengths.append(len(row[0]))
	for row in notSpamCopy:
		allCopy.append(row[0])
		lengths.append(len(row[0]))
	if (len(lengths)<(2*int(n))):
		print ("TOO FEW SAMPLES IN DATABASE, CHOOSE SMALLER n")
		return
	lengths = np.array(lengths)
	n = int(n)
	y1 = np.zeros(n)
	y2 = np.ones(n)
	y = np.	concatenate((y1,y2),axis=0)
	vectorizer = CountVectorizer(analyzer='word', min_df=3, decode_error='ignore')
	#print lengths.shape
	spamFeatures = vectorizer.fit_transform(allCopy)
	#spamFeatures = np.concatenate(([spamFeatures],[lengths]),axis=1)
	#print vectorizer.get_feature_names()
	print "DICTIONARY LENGTH: %i " %spamFeatures.shape[1]
	#print notSpamFeatures.shape, type(notSpamFeatures)
	feature_names = vectorizer.get_feature_names()
	X_train, X_test, y_train, y_test = train_test_split(spamFeatures, y, test_size=0.2)  
	clf = svm.SVC()
	clf.fit(X_train, y_train)
	y_predicted = clf.predict(X_test)
	from sklearn import metrics
	print ("ZERO IS SPAM, ONE IS NOT SPAM")
	print 'ACCURACY:', metrics.accuracy_score(y_test, y_predicted)
	print metrics.classification_report(y_test, y_predicted)
	print
	print 'CONFUSION \n'
	print pd.DataFrame(metrics.confusion_matrix(y_test, y_predicted))
	f = open('SVMclassifier.pickle', 'wb')
	pickle.dump(clf, f)
	f.close()
	
if __name__ == '__main__':
	n = int(sys.argv[1])
	build(n)
	#classifier = nltk.NaiveBayesClassifier.train(trainingData)
