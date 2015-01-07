#make this DFS
#randomize WP seed (including languages)

import re, urllib, random, webbrowser, reportlab

def crawl (x):
	global urlBank
	global pdfBank
	for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(x).read(), re.I):
		# print i
		y = re.search('\.pdf' , i)
		if y:
			#webbrowser.open(i)
			pdfBank.append(i)
			print("found! pdfBank length is %d" %len(pdfBank))
			return
		y = re.match('http://' , i)
		if y:
			urlBank.append(i)
	print ("There are now %d items in urlBank" %len(urlBank))
	return
	

urlBank = []
pdfBank = []
url = 'http://en.wikipedia.org/wiki/Special:Randompage'
crawl(url)
done = 0
x = 3

while done ==0 :
	x = random.randrange(0, len(urlBank))
	print ("CRAWLING " + urlBank[x] + "\n")
	urlBank.remove(urlBank[x])
	crawl(urlBank[x])
	if len(pdfBank) >= x:
		pdfList = open('output.txt', 'w')
		done = 1
		for i in pdfBank:	
			pdfList.write(i)
			pdfList.close()
