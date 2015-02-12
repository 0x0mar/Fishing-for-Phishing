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

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

def buildDicts(n):
	i = 0 
	noTagsDict = set()
	tagsDict = set()
	while (i<n):
		if (os.path.isfile("spam/%d.txt" %i)):
				try:
					readInFile = open("spam/%d.txt" %i)
					content = readInFile.read()
					noSymbols = re.sub('[^A-Za-z-]+', ' ', content.lower()) #noSymbols is stripped of symbols
					allCopy = set(noSymbols.split()) #allCopy is the set of words without symbols
					noTags=cleaner.clean_html(content)  
					noTags = re.sub('[^A-Za-z-]+', ' ', noTags.lower())
					noTagsSet = set(noTags.split())
					tags = allCopy.difference(noTagsSet)
					noTagsDict = noTagsDict.union(noTagsSet)
					tagsDict = tagsDict.union(tags)
				except Exception, err:
					print traceback.format_exc()
    				print sys.exc_info()[0]
		i = i+1	
	noTagsFile = open('noTagsdict.txt', 'w')
	tagsFile = open('tagsDict.txt', 'w')
	noTagsFile.write (str(noTagsDict))
	noTagsFile.close()
	tagsFile.write (str(tagsDict))
	tagsFile.close()
	return (n, tagsDict, noTagsDict)
		
def tokenize(n, tagsDict, noTagsDict):
	i=0
	df = pandas.DataFrame(columns=['tags','noTags','target'])

	while (i<n):
		tagsVector={}
		noTagsVector={}
		allVector={}
		if (os.path.isfile("spam/%d.txt" %i)):
			try:
				for word in tagsDict:
					tagsVector[word] = 0
					allVector[word] = 0
				for word in noTagsDict:
					noTagsVector[word] = 0
					allVector[word] = 0	
				readInFile = open("spam/%d.txt" %i)
				content = readInFile.read()
				noSymbols = re.sub('[^A-Za-z-]+', ' ', content.lower()) #noSymbols is stripped of symbols
				allCopy = noSymbols.split() #allCopy is the set of words without symbols
				noTags=cleaner.clean_html(content)  
				noTags = re.sub('[^A-Za-z-]+', ' ', noTags.lower())
				noTagsSet = noTags.split()
				for tag in noTagsSet:
					noTagsVector[tag] = noTagsVector[tag] + 1
				for tag in allCopy:
					allVector[tag] = allVector[tag] + 1
				for tag in tagsDict:
					tagsVector[tag] = allVector[tag] - noTagsVector.get(tag, 0)
				print ("tags vector")
				print(tagsVector)
				print ("no tags vector")
				print(noTagsVector)
				df[i] = (tagsVector.values(), noTagsVector.values(), 'spam')
				
			except Exception, err:
				print traceback.format_exc()
    			print sys.exc_info()[0]
		i = i+1		
	print(df)
if __name__ == '__main__':
	n = int(sys.argv[1])
	n,tagsDict,noTagsDict = buildDicts(n)
	tokenize(n,tagsDict,noTagsDict)