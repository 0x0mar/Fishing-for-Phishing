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
import pandas

def buildDicts(n):
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True
	i = 0 
	tagsDict = set()
	while (i < n):
		if (os.path.isfile("spam/%d.txt" % i)):
			try:
				readInFile = open("spam/%d.txt" % i)
				content = readInFile.read()
				noSymbols = re.sub('[^A-Za-z-]+', ' ', content.lower())  # noSymbols is stripped of symbols
				tags = set(noSymbols.split())  # allCopy is the set of words without symbols
				tagsDict = tagsDict.union(tags)
			except Exception, err:
				print traceback.format_exc()
				print sys.exc_info()[0]
		if (os.path.isfile("notspam/%d.txt" % i)):
			try:
				readInFile = open("notspam/%d.txt" % i)
				content = readInFile.read()
				noSymbols = re.sub('[^A-Za-z-]+', ' ', content.lower())  # noSymbols is stripped of symbols
				tags = set(noSymbols.split())  # allCopy is the set of words without symbols
				tagsDict = tagsDict.union(tags)
			except Exception, err:
				print traceback.format_exc()
				print sys.exc_info()[0]
		i = i + 1
		print (i)
    	
   	return (n, tagsDict)
		
def tokenize(n, tagsDict):
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True
	i = 0
	df = pandas.DataFrame(columns=[list(tagsDict)])

	while (i < n):
		allVector = {}
		if (os.path.isfile("spam/%d.txt" % i)):
			try:
				for word in tagsDict:
					allVector[word] = 0
				readInFile = open("spam/%d.txt" % i)
				content = readInFile.read()
				noSymbols = re.sub('[^A-Za-z-]+', ' ', content.lower())  # noSymbols is stripped of symbols
				allCopy = noSymbols.split()  # allCopy is the set of words without symbols
				for tag in allCopy:
					df.ix[i[tag]] = df.ix[i[tag]]  + 1
				df.ix[i['isSpam']] = 'spam'
				
			except Exception, err:
				print traceback.format_exc()
    			print sys.exc_info()[0]
		
		i = i + 1		
	print(df)
	return(df)
	
if __name__ == '__main__':
	n = int(sys.argv[1])
	n, tagsDict = buildDicts(n)
	data = tokenize(n, tagsDict)
	trainingData = data [:(n*3/4)]
	testData = data [(n*3/4)+1:n]
	classifier = nltk.NaiveBayesClassifier.train(trainingData)
