from pygoogle import pygoogle as pyg
import random
from os import listdir
import PyPDF2 as pdf
import urllib2
import urllib
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')

def generateList(num):
	global urlBank
	global pdfBank
	urlBank = ['http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Arabic/','http://www.dmoz.org/World/Norsk/','http://www.dmoz.org/World/Catal%C3%A0/','http://www.dmoz.org/World/Esperanto/','http://www.dmoz.org/World/Rom%C3%A2n%C4%83/','http://www.dmoz.org/World/Suomi/','http://en.wikipedia.org/wiki/Special:Randompage', 'http://es.wikipedia.org/wiki/Special:Randompage',  'http://de.wikipedia.org/wiki/Special:Randompage' ,  'http://zh.wikipedia.org/wiki/Special:Randompage' ,  'http://pt.wikipedia.org/wiki/Special:Randompage',  'http://pl.wikipedia.org/wiki/Special:Randompage',  'http://it.wikipedia.org/wiki/Special:Randompage',  'http://ja.wikipedia.org/wiki/Special:Randompage',  'http://ru.wikipedia.org/wiki/Special:Randompage']
	pdfBank = []
	done = 0

	while done ==0 :
		if len(urlBank) > 1000:
			urlBank = ['http://www.dmoz.org/World/Ukrainian/','http://www.dmoz.org/World/Arabic/','http://www.dmoz.org/World/Norsk/','http://www.dmoz.org/World/Catal%C3%A0/','http://www.dmoz.org/World/Esperanto/','http://www.dmoz.org/World/Rom%C3%A2n%C4%83/','http://www.dmoz.org/World/Suomi/','http://en.wikipedia.org/wiki/Special:Randompage', 'http://es.wikipedia.org/wiki/Special:Randompage',  'http://de.wikipedia.org/wiki/Special:Randompage' ,  'http://zh.wikipedia.org/wiki/Special:Randompage' ,  'http://pt.wikipedia.org/wiki/Special:Randompage',  'http://pl.wikipedia.org/wiki/Special:Randompage',  'http://it.wikipedia.org/wiki/Special:Randompage',  'http://ja.wikipedia.org/wiki/Special:Randompage',  'http://ru.wikipedia.org/wiki/Special:Randompage']
		x = random.randrange(0, len(urlBank))
		#print ("CRAWLING " + urlBank[x] + "\n")
		try:
			for i in re.findall('''href=["'](.[^"']+)["']''', urllib2.urlopen(urlBank.pop(x)).read(200000), re.I):
			# print i
				z = re.match('http://' , i)
				if z:
					urlBank.append(i)
					y = re.search('\.pdf' , i)
					if y:
						#webbrowser.open(i)
						pdfBank.append(i)
						#print("found! pdfBank length is %d" %len(pdfBank))
			#print ("There are now %d items in urlBank" %len(urlBank))
		except:
			continue
		
		if len(pdfBank) >= num:
			pdfList = open('urls.txt', 'w')
			done = 1
			for i in pdfBank:	
				pdfList.write("%s \n" % i)
			pdfList.close()
	print ("finished!")
	return pdfBank
	
def downloadRandom():
	lines = open('urls.txt').read().splitlines()
	x = 0
	for i in lines:
		x = x +1
		urllib.urlretrieve(i, './downloads/%d.pdf' %x) 

def generateSplice():
    print ' > Splicing files...\n > (Ignore errors)'
    newPdf = pdf.PdfFileMerger(strict=False)
    files = [x for x in listdir('./downloads/') if x != '.DS_Store']

    if len(files) == 0:
        sys.exit(' > You must first download some files.')

    for x in files:
        f = pdf.PdfFileReader(file('./downloads/'+x, 'rb'), strict=False)
        try:
            pn = random.randint(0,f.getNumPages()-1)
        except pdf.utils.PdfReadError:
            continue
        try:
            newPdf.merge(0,'./downloads/'+x,pages=(pn,pn+1))
        except (pdf.utils.PdfReadError, ValueError):
            continue
            
    newPdf.write('spliced.pdf')
    newPdf.close()
    print ' > Done!'

if __name__ == '__main__':
    try:
        m = sys.argv[1]
    except Exception:
        sys.exit(' > You must enter \'search\', \'download\', or \'splice\' (without quotation marks).')
    if m == 'search':
        generateList(5)
    elif m == 'download':
        downloadRandom()
    elif m == 'splice':
        generateSplice()
    else:
        sys.exit(' > You must enter \'search\', \'download\', or \'splice\' (without quotation marks).')
