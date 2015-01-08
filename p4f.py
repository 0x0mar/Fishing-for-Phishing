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

def crawl():
	cleaner = Cleaner(javascript = True, style = True, allow_tags=[''], remove_unknown_tags=False)
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	for row in seed:
		try:
			content = urllib2.urlopen(row["url"], timeout=3).read(20000)	
			bank = open('%d.txt' %i, 'w')
			content = (cleaner.clean_html(content) + "******************* \n FROM %s" %row["url"])
			bank.write (content)
			print row["url"] + " success! \n"
			bank.close()
		except:
			content = " "
			print "broken link"
		
if __name__ == '__main__':
	crawl()
