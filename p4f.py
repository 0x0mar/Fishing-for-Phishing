import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	wl = []
	seed = []
	with open('wl.csv', 'rb') as csvfile:
		wlreader = csv.reader(csvfile, delimiter=',')
		for row in wlreader:
			string=(row[1].split("/"))[0]
			wl.append(string)
	db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
	cursor = db.cursor()
	i = 0 
	outLinks = []
	cleaner = Cleaner(javascript = True, style = True, allow_tags=[''], remove_unknown_tags=False)
	if (n ==0):
		json_seed = open('seed.json', 'rb')
		seedx = json.load(json_seed)
		for row in seedx:
			seed += row
	else:
		execString = ("SELECT URLTo FROM outboundLinks WHERE lvl=%i;" % (n)) 
		cursor.execute(execString)
		seed = cursor.fetchall()
	for row in seed:
		try:
			i += 1
			url = row["url"]
			domain = (url.split("/"))[2]
			content = urllib2.urlopen(url, timeout=3).read(20000)	
			for k in re.findall('''href=["'](.[^"']+)["']''', content):
				z = re.match('http://' , k)
				if z:
					if ((domain + "/") in wl):
						print ("Whitelisted \n")
						bad = 0
					else:
						bad =1
					domainTo = (z.split("/"))[2]
					execString = ("INSERT INTO outboundLinks (Lvl, Domain, domainTo, URL, URLto, CopySource, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', 'crawl', 'false', '%i');" % ((n+1),domain,domainTo, url, k, bad)) 
					cursor.execute(execString)
			bank = open('spam/%d.txt' %i, 'w')
			content = (cleaner.clean_html(content) + "******************* \n FROM %s" %url)
			bank.write (content)
			execString = ("INSERT INTO Content (Lvl, Content, Domain, domainTo, URL, CopySource) VALUES ('%i', , '%s', '%s', '%s', '%s', 'crawl');" % ((n+1), content, domain,domainTo, url)) 
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
	n = int(sys.argv[1])
	crawl(n)
	
