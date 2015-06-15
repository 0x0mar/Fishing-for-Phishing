From the command line, "python FishingForPhishing.py COMMAND" allows you use any of the features of Fishing for Phishing.

"python FishingForPhishing.py seed" 
Iterates through files called seed.csv and safeSeed.csv and adds each link to the seed and safe seed tables respectively. 

"python FishingForPhishing.py emailseed" 
If locally stored credentials for a gmail account are available, emailseed reads the body of each email tagged as spam, adding any link to the spam outboundLinks table and adding all copy to the spam content table.

"python FishingForPhishing.py whitelist"
Iterates through every site stored in a file called wl.csv, adding the sites to the whitelist table in the database. These should be high-traffic sites that are almost certainly not spam. 

"python FishingForPhishing.py crawl" 
Begins by visiting every page in the spam seed, adding any links encountered to the outboundLinks table and all site copy to the content table. Then, it continues by crawling outward along those links and adding more links add copy to the database. As links are visited, the crawled field in the database is updated so they are not crawled again. All links are checked against the whitelist stored in the database; if they are high-traffic sites found in that table, they are marked as "not to spam" in the table.

"python FishingForPhishing.py safecrawl" 
Same as crawl, but starts in the safe seed and checks the Google Safe Browsing API rather than a whitelist. The SafeBrowsing API will alert the crawler if an unsafe site is visited, so the page can be stored in the spam tables rather than the safe tables.

"python FishingForPhishing.py SVM n"
Builds a classifier using n samples from safeContent and n samples from spam content. .8 * n samples of each are used in training, and the rest are used to test the accuracy of the classifier. The classifier is stored in a pickle file called SVMclassifier, which can be used to make further predictions. 

"python FishingForPhishing.py NB n"
Builds a classifier using n samples from safeContent and n samples from spam content. .8 * n samples of each are used in training, and the rest are used to test the accuracy of the classifier. The classifier is stored in a pickle file called NBclassifier, which can be used to make further predictions. The 10 features that are most useful in the classification are also displayed. 
