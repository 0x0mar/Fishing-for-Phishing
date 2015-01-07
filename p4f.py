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

reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	pseed = []
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	bank = open('bank.txt', 'w')
	for row in seed:
		pseed.append(row["url"])
		bank.write (lxml.html.tostring(cleaner.clean_html(lxml.html.parse(row["url"]))) + "****************** \n")
		
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
