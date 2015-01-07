import re, urllib, random, webbrowser, urllib2, sys

def crawl (x):
	global urlBank
	global pdfBank
	try:
		for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(x).read(200000), re.I):
			# print i
			z = re.match('http://' , i)
			if z:
				urlBank.append(i)
				y = re.search('\.pdf' , i)
				if y:
					#webbrowser.open(i)
					pdfBank.append(i)
					print("found! pdfBank length is %d" %len(pdfBank))
		#print ("There are now %d items in urlBank" %len(urlBank))
	except:
		return

urlBank = ['http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Arabic/','http://www.dmoz.org/World/Norsk/','http://www.dmoz.org/World/Catal%C3%A0/','http://www.dmoz.org/World/Esperanto/','http://www.dmoz.org/World/Rom%C3%A2n%C4%83/','http://www.dmoz.org/World/Suomi/','http://en.wikipedia.org/wiki/Special:Randompage', 'http://es.wikipedia.org/wiki/Special:Randompage',  'http://de.wikipedia.org/wiki/Special:Randompage' ,  'http://zh.wikipedia.org/wiki/Special:Randompage' ,  'http://pt.wikipedia.org/wiki/Special:Randompage',  'http://pl.wikipedia.org/wiki/Special:Randompage',  'http://it.wikipedia.org/wiki/Special:Randompage',  'http://ja.wikipedia.org/wiki/Special:Randompage',  'http://ru.wikipedia.org/wiki/Special:Randompage']
pdfBank = []
done = 0
num = int(sys.argv[1])

while done ==0 :
	if len(urlBank) > 1000:
		urlBank = ['http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Arabic/','http://www.dmoz.org/World/Norsk/','http://www.dmoz.org/World/Catal%C3%A0/','http://www.dmoz.org/World/Esperanto/','http://www.dmoz.org/World/Rom%C3%A2n%C4%83/','http://www.dmoz.org/World/Suomi/','http://en.wikipedia.org/wiki/Special:Randompage', 'http://es.wikipedia.org/wiki/Special:Randompage',  'http://de.wikipedia.org/wiki/Special:Randompage' ,  'http://zh.wikipedia.org/wiki/Special:Randompage' ,  'http://pt.wikipedia.org/wiki/Special:Randompage',  'http://pl.wikipedia.org/wiki/Special:Randompage',  'http://it.wikipedia.org/wiki/Special:Randompage',  'http://ja.wikipedia.org/wiki/Special:Randompage',  'http://ru.wikipedia.org/wiki/Special:Randompage']
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl(urlBank.pop(x))

	if len(pdfBank) >= num:
		pdfList = open('output.txt', 'w')
		done = 1
		for i in pdfBank:	
			pdfList.write("%s \n" % i)
		pdfList.close()

print ("finished!")
