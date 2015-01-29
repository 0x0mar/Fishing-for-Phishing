import urllib2, sys, re, csv, json, lxml, lxml.html
from lxml.html.clean import Cleaner
import MySQLdb, sys
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()
reload(sys)
sys.setdefaultencoding('utf8')

def crawl(n):
	i=0
	seed = []
	db = MySQLdb.connect(host='cspp53001.cs.uchicago.edu',db='jcbraunDB',user='jcbraun',passwd='3312crystal')
	cursor = db.cursor()
	outLinks = []
	if (n ==0):
		execString = ("SELECT URL, Domain FROM safeSeed WHERE crawled=0;") 
		cursor.execute(execString)
		seedx = cursor.fetchall()
	else:
		execString = ("SELECT URLTo FROM safeOutboundLinks WHERE lvl=%i AND toSpam=0;" % (n)) 
		cursor.execute(execString)
		seedx = cursor.fetchall()

	for row in seedx:
		i = 1+1
		try:
			url = row[0]
			print url
			domain = get_tld(url, fail_silently=True)
			content = urllib2.urlopen(url, timeout=3).read(20000)
			for k in re.findall('''href=["'](.[^"']+)["']''', content):
				z = re.match('http://' , k)
				if z:
					domainTo = (get_tld(k, fail_silently=True))
					print "domainTo is: %s" %domainTo
					reqURL = "https://sb-ssl.google.com/safebrowsing/api/lookup?client=f4p&key=AIzaSyCD0pNAG-6HVh_W6udGYZFz-2_p0yHDD5k&appver=31&pver=3.1&url=" + k
					response = urllib2.urlopen(reqURL).getcode()
					if (response==200):
						print ("Found dangerous site \n")
						bad = 1
						execString = ("INSERT INTO inboundLinks (Domain, domainTo, URL, URLto, Crawled) VALUES ('%s', '%s', '%s', '%s', 'false');" % (domain, domainTo, url, k))
						cursor.execute(execString)
					else:
						bad = 0
						execString = ("INSERT INTO safeOutboundLinks (Lvl, Domain, domainTo, URL, URLto, Crawled, toSpam) VALUES ('%i', '%s', '%s', '%s', '%s', '0', '%i');" % ((n+1), domain, domainTo, url, k, bad))
						cursor.execute(execString)
			bank = open('notspam/%d.txt' %i, 'w')
			bank.write (content)
			content=db.escape_string(content)
			execString = ("INSERT INTO safeContent (Lvl, Content, Domain, URL, CopySource) VALUES ('%i', '%s', '%s', '%s', 'crawl');" % ((n+1), content, domain, url)) 
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
	
