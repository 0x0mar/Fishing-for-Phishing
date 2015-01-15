import re, urllib, random, webbrowser, urllib2, sys
import json

phishListParsed = []
json_list = open('seed.json', 'rb')
phishList = json.load(json_list)
for row in phishList:
	phishListParsed.append(row['url'])

urlBank = ['http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Arabic/','http://www.dmoz.org/World/Norsk/','http://www.dmoz.org/World/Catal%C3%A0/','http://www.dmoz.org/World/Esperanto/','http://www.dmoz.org/World/Rom%C3%A2n%C4%83/','http://www.dmoz.org/World/Suomi/','http://en.wikipedia.org/wiki/Special:Randompage', 'http://es.wikipedia.org/wiki/Special:Randompage',  'http://de.wikipedia.org/wiki/Special:Randompage' ,  'http://zh.wikipedia.org/wiki/Special:Randompage' ,  'http://pt.wikipedia.org/wiki/Special:Randompage',  'http://pl.wikipedia.org/wiki/Special:Randompage',  'http://it.wikipedia.org/wiki/Special:Randompage',  'http://ja.wikipedia.org/wiki/Special:Randompage',  'http://ru.wikipedia.org/wiki/Special:Randompage']
phishBank = []
done = 0

while done == 0:
	if len(urlBank) > 1000:
		urlBank [:100]
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	crawl = urlBank.pop(x)

	if len(phishBank) >= 3:
		phishList = open('output.txt', 'w')
		done = 1
		for i in phishBank:	
			phishList.write("%s \n" % i)
		phishList.close()


	for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(crawl).read(200000), re.I):
		z = re.match('http://' , i)
		if z:
			print i
			urlBank.append(i)
			for row in phishListParsed:
				print "i is " + i + "\n"
				print "row is " + row + "\n"
				y = re.search(row, i)
				if y:
					phishBank.append(i)
					print("found! pdfBank length is %d" %len(phishBank))
print ("finished!")

