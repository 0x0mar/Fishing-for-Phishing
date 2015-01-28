import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	wl = []
	seed = []
	with open('wl.csv', 'rb') as csvfile:
		wlreader = csv.reader(csvfile, delimiter=',')
		for row in wlreader:
			wl.append(get_tld(row[1], fail_silently=true))
			print ("Adding " + get_tld(row[1], fail_silently=true) + "\n")
	db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
	cursor = db.cursor()
	i = 0 
	outLinks = []
	if (n ==0):
		execString = ("SELECT URL, Domain FROM seed WHERE crawled=0;") 
		cursor.execute(execString)
		seedx = cursor.fetchall()
	else:
		execString = ("SELECT URLTo FROM outboundLinks WHERE lvl=%i;" % (n)) 
		cursor.execute(execString)
		seedx = cursor.fetchall()

	for row in seedx:
		try:
			i += 1
			url = row[0]
			domain = get_tld(url, fail_silently=true)
			if (url.startswith("www")):
				url = url [4:]
			content = urllib2.urlopen(url, timeout=3).read(20000)	
			for k in re.findall('''href=["'](.[^"']+)["']''', content):
				z = re.match('http://' , k)
				if z:
					domainTo = (get_tld(k))
					print "domainTo is: %s" %k
					if (domain in wl):
						print ("Whitelisted \n")
						bad = 0
					else:
						bad =1
					execString = ("INSERT INTO outboundLinks (Lvl, Domain, domainTo, URL, URLto, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', 'false', '%i');" % ((n+1), domain, domainTo, url, k, bad))
					cursor.execute(execString)
			bank = open('spam/%d.txt' %i, 'w')
			bank.write (content)
			content=db.escape_string(content)
			execString = ("INSERT INTO Content (Lvl, Content, Domain, URL, CopySource) VALUES ('%i', '%s', '%s', '%s', 'crawl');" % ((n+1), content, domain, url)) 
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
	
