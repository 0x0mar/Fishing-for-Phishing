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
	i = 0 
	cleaner = Cleaner(javascript = True, style = True, allow_tags=[''], remove_unknown_tags=False)
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	outLinks = []		
	for row in seed:
		try:
			i += 1
			content = urllib2.urlopen(row["url"], timeout=3).read(20000)	
			bank = open('%d.txt' %i, 'w')
			content = (cleaner.clean_html(content) + "******************* \n FROM %s" %row["url"])
			bank.write (content)
			print row["url"] + " success! \n"
			for i in re.findall('''href=["'](.[^"']+)["']''', content):
				z = re.match('http://' , i)
				if z:
					print "Adding %s to link bank" %i
					outLinks += i
			print i
			urlBank.append(i)
			bank.close()
		except:
			print ("Broken link")	
		
if __name__ == '__main__':
	crawl()
