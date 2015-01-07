from os import listdir
import urllib2
import sys
import re
import json
import lxml
import lxml.html
from lxml.html.clean import Cleaner


cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

def crawl(n):
	pseed = []
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	for row in seed:
		i = i + 1
		bank2 = open('bank2.txt', 'a')
		print "trying: " + row["url"] + "\n"
		if i == n
			return
		try:
			print row["url"] + " success! \n"
			bank2.write (lxml.html.tostring(cleaner.clean_html(lxml.html.parse(row["url"]))))	
		except:
			print "broken link"
		
if __name__ == '__main__':
    try:
        m = sys.argv[1]
    except Exception:
        sys.exit(' > Enter search and an integer')
    if m == 'search':
		if len(sys.argv) == 3:
			n = sys.argv[2]
			crawl(n)
		else:
			print ("Enter a number of items to search for")
