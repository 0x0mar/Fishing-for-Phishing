from os import listdir
import sys
import re
import json
import lxml, MySQLdb
import lxml.html
from lxml.html.clean import Cleaner
import nltk
from nltk.tokenize import RegexpTokenizer

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

def tokenizer():
	print ("querying")
	db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
	cursor = db.cursor()
	execString = ("SELECT Content FROM Content WHERE Lvl=1;") 
	cursor.execute(execString)
	copy = cursor.fetchall()
	print ("queried")
	noTagsDict = set()
	for row in copy:
		noTagsFile = open('dict.txt', 'w')
		tagsFile = open('tagsDict.txt', 'w')
		noSymbols = re.sub('[^A-Za-z0-9]+', '', row[0])
		tokenizer = RegexpTokenizer(r'\w+')
		tokenized = tokenizer.tokenize(noSymbols)
		allCopy = set(tokenized)
		noTags=(lxml.html.tostring(cleaner.clean_html(lxml.html.parse(row[0]))))
		noTagsTokened = tokenizer.tokenize(noTags)
		tags = allCopy - noTagsTokened
		noTagsDict = noTagsDict + set(noTags)
		noTagsFile.write (noTagsDict)
		noTagsFile.close()
		print ("*")

if __name__ == '__main__':
	tokenizer()
