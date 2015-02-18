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

		
def tokenize(n):
	reload(sys)
	sys.setdefaultencoding('utf8')
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True
	i = 0
	allCopy = list()
	
	db = MySQLdb.connect(host='127.0.0.1',db='jcbraunDB',user='root',passwd='3312crystal')
	cursor = db.cursor()
	execString = ("SELECT Content FROM Content ORDER BY RAND() LIMIT %s;"%n) 
	cursor.execute(execString)
	spamCopy = cursor.fetchall()
	execString = ("SELECT Content FROM safeContent ORDER BY RAND() LIMIT %s;"%n) 
	cursor.execute(execString)
	notSpamCopy = cursor.fetchall()
	for row in spamCopy:
		allCopy.append(row[0])
	for row in notSpamCopy:
		allCopy.append(row[0])
	
	y1=['0'] * n
	y2=['1'] * n
	y = y1+y2
	vectorizer = CountVectorizer(analyzer='word', min_df=3, decode_error='ignore')
	spamFeatures = vectorizer.fit_transform(allCopy)
	#print vectorizer.get_feature_names()
	print spamFeatures.shape, type(spamFeatures)
	#print notSpamFeatures.shape, type(notSpamFeatures)
	feature_names = vectorizer.get_feature_names()
	X_train, X_test, y_train, y_test = train_test_split(spamFeatures, y, test_size=0.2)  
	clf = MultinomialNB()
	clf.fit(X_train, y_train)
       	top10 = np.argsort(clf.coef_[0])[-10:]
       	print("%s: %s" % ("spam features"," ".join(feature_names[j] for j in top10)))
	y_predicted = clf.predict(X_test)
	from sklearn import metrics
	print 'Accuracy:', metrics.accuracy_score(y_test, y_predicted)
	print metrics.classification_report(y_test, y_predicted)
	print
	print 'confusion \n'
	print pd.DataFrame(metrics.confusion_matrix(y_test, y_predicted))
	
if __name__ == '__main__':
	n = int(sys.argv[1])
	tokenize(n)
	#classifier = nltk.NaiveBayesClassifier.train(trainingData)
