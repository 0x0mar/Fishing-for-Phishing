from os import listdir
import urllib2
import sys
import re
import json
import lxml
import lxml.html
from lxml.html.clean import Cleaner
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True
	cleaner.allow_tags=['']
	cleaner.remove_unknown_tags=False
	pseed = []
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	i = 0
	for row in seed:
		i = i + 1
		if i == n:
			break
		try:
			content = urllib2.urlopen(row["url"], timeout=3).read(20000)	
			bank = open('/spam/%d.txt' %i, 'w')
			content = (cleaner.clean_html(content) + "******************* \n FROM %s" %row["url"])
			bank.write (content)
			print row["url"] + " success! \n"
			bank.close()
		except:
			content = " "
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
