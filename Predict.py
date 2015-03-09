def NBpredict(content):
    vectorizer = CountVectorizer(analyzer='word', min_df=3, decode_error='ignore')
    vector = vectorizer.fit_transform(content)
    f = open('NBclassifier.pickle')
    clf = pickle.load(f)
    f.close()
    predicted = clf.predict(vector)
    print predicted
    
def SVMpredict(content):
    vectorizer = CountVectorizer(analyzer='word', min_df=3, decode_error='ignore')
    vector = vectorizer.fit_transform(content)
    f = open('SVMclassifier.pickle')
    clf = pickle.load(f)
    f.close()
    predicted = clf.predict(vector)
    print predicted
    
def getContent (url):
    content = urllib2.urlopen(url, timeout=3).read(200000)
    
if __name__ == '__main__':
    content = getContent(sys.argv[2])
    if sys.argv[1]=="NB":
        crawl(content)
    elif sys.argv[1]=="SVM":
        safeCrawl(content)