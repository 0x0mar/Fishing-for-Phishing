import urllib2
import sys
import re
import csv
import json
import lxml
import lxml.html
from lxml.html.clean import Cleaner
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def crawl():
	wl = []
	with open('wl.csv', 'rb') as csvfile:
		wlreader = csv.reader(csvfile, delimiter=',')
		for row in wlreader:
			wl.append(row[1])
	db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
	cursor = db.cursor()
	i = 0 
	outLinks = []
	cleaner = Cleaner(javascript = True, style = True, allow_tags=[''], remove_unknown_tags=False)
	json_seed = open('seed.json', 'rb')
	seed = json.load(json_seed)
	for row in seed:
		try:
			i += 1
			url = row["url"]
			domain = (url.split("/"))[2]
			content = urllib2.urlopen(url, timeout=3).read(20000)	
			for k in re.findall('''href=["'](.[^"']+)["']''', content):
				z = re.match('http://' , k)
				if z:
					print "Adding %s to link bank" %k
					outLinks += k
					if (domain + "/" in wl):
						bad = 0
					else:
						bad =1
					execString = ("INSERT INTO outboundLinks (Lvl, Domain, URL, URLto, CopySource, Crawled, toSpam) VALUES ('0', '%s', '%s', '%s', 'crawl', 'false', '%i');" % (domain, url, k, bad)) 
					cursor.execute(execString)
			bank = open('spam/%d.txt' %i, 'w')
			content = (cleaner.clean_html(content) + "******************* \n FROM %s" %url)
			bank.write (content)
			execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('0', '%s', '%s', '%s', 'crawl');" % (content, domain, url)) 
			cursor.execute(execString)
			print url + " success! \n"
			bank.close()
			db.commit()
		except Exception as e:
			print ("Broken link to %s" %url)	
			print (type(e))
			print (e.args)
	db.close()
if __name__ == '__main__':
	
	crawl()
	
