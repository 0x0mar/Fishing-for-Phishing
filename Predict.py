import urllib2, sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import numpy as np
import pickle

def NBpredict(content):
    vectorizer = CountVectorizer(analyzer='word', min_df=3, decode_error='ignore')
    f = open('NBclassifier.pickle')
    clf = pickle.load(f)
    f.close()
    predicted = clf.predict(vector)
    print predicted
    
def SVMpredict(content):
    sample = []
    sample.append(content)
    f = open('SVMclassifier.pickle')
    clf = pickle.load(f)
    f.close()
    f = open('SVMvocab.pickle')
    vectorizer = pickle.load(f)
    vector = vectorizer.transform(sample)
    predicted = clf.predict(vector)
    f.close()
    print predicted
    return str(predicted)
    
def getContent (url):
    return urllib2.urlopen(url, timeout=3).read(200000)

def getContentPredict (url):
    return SVMpredict(urllib2.urlopen(url, timeout=3).read(200000))
    
if __name__ == '__main__':
    content = getContent(sys.argv[2])
    print "CONTENT" + content
    if sys.argv[1]=="NB":
        NBpredict(content)
    elif sys.argv[1]=="SVM":
        SVMpredict(content)