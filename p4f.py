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
	bank = open('bank .txt', 'w')
	bank2 = open('bank2.txt', 'w')
	i = 0
	for row in seed:
		i = i + 1
		if i == n:
			break
		try:
			content = urllib2.urlopen(row["url"], timeout=3).read(20000)
		except:
			print "broken link"
		try:	
			bank = open('bank.txt', 'a')
			content = (cleaner.clean_html(content))
			content = " ".join(content.split())
			document = lxml.html.document_fromstring(content)
			content = "\n **************** \n FROM: %s" %row['url'] + "\n" + document.text_content()
			bank.write (content)
			print row["url"] + " success! \n"
			bank.close()
		except:
			print "didn't write"
			
		
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
