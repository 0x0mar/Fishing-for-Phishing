from os import listdir
import os.path
import sys, traceback
import re
import json
import lxml, MySQLdb
import lxml.html
from lxml.html.clean import Cleaner
import nltk
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import numpy as np

		
def tokenize(n):
	reload(sys)
	sys.setdefaultencoding('utf8')
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True
	i = 0
	existingSpam = list()
	existingNotSpam = list()
	while (i < n):
		if (os.path.isfile("spam/%d.txt" % i)):
			existingSpam.append("spam/" + str(i) + ".txt")
		if (os.path.isfile("notspam/%d.txt" % i)):
			existingNotSpam.append("notspam/" + str(i) + ".txt") 
		i = i + 1
	y1=['spam'] * len(existingSpam)
	y2=['notSpam'] * len(existingNotSpam)
	y = y1+y2	
	existingSpam = existingSpam + existingNotSpam
	vectorizer = CountVectorizer(analyzer='word', input='filename', min_df=3, decode_error='ignore')
	spamFeatures = vectorizer.fit_transform(existingSpam)
	#print vectorizer.get_feature_names()
	print spamFeatures.shape, type(spamFeatures)
	#print notSpamFeatures.shape, type(notSpamFeatures)
	X_train, X_test, y_train, y_test = train_test_split(spamFeatures, y, test_size=0.2)  
	clf = LogisticRegression()
	clf.fit(X_train, y_train)
	y_predicted = clf.predict(X_test)
	from sklearn import metrics
	print 'Accuracy:', metrics.accuracy_score(y_test, y_predicted)
	print
	print metrics.classification_report(y_test, y_predicted)
	print
	print 'confusion matrix'
	print
	print pd.DataFrame(metrics.confusion_matrix(y_test, y_predicted))
	
if __name__ == '__main__':
	n = int(sys.argv[1])
	tokenize(n)
	#classifier = nltk.NaiveBayesClassifier.train(trainingData)
