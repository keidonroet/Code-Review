from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from requests_html import HTMLSession
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk

session = HTMLSession()
#import urllib3
url = 'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en'
#http = urllib3.PoolManager()

#resp = http.request('GET', url)
#print(resp.data.decode('utf-8'))

r = session.get(url)

r.html.render(sleep=1, scrolldown=5)

articles = r.html.find('article')
#print(articles)
title_words = []
for item in articles:
    try:
        newsitem = item.find('h3', first=True)
        title = newsitem.text
        #link = newsitem.absolute_links
        title_words.append(title.split())
        #print(title)
    except:
        pass

#print(title_words)
reg_list = []
for x in title_words:
    for item in x:
        reg_list.append(item)
#print(reg_list)

for i in range(len(reg_list)):
    reg_list[i] = reg_list[i].lower()

stop_words = open('stopwords_en.txt', 'r')
stop_list = []
for line in stop_words:
    stripped_line = line.strip()
    line_list = stripped_line.split()
    stop_list.append(line_list)
#print(stop_list)
new_list = []
for x in stop_list:
    for item in x:
        new_list.append(item)
#print(new_list)

for word in list(reg_list):
    if word in new_list:
        reg_list.remove(word)
    if word.isdigit() is True:
        reg_list.remove(word)
print(reg_list)

string = ""
for word in reg_list:
    string = string + word + " "
#print(string)

bigrams = []
#bigrams
for i in range(len(reg_list)):
    try:
        bigrams.append(reg_list[i] + "_" + reg_list[i+1])
    except:
        pass
reg_list.extend(bigrams)

#sentiment
analyzer = SentimentIntensityAnalyzer()
vad_sentiment = analyzer.polarity_scores(string)

pos = vad_sentiment['pos']
neg = vad_sentiment['neg']
neu = vad_sentiment['neu']

print('It is positive for', '{:.1%}'.format(pos))
print('It is negative for', '{:.1%}'.format(neg))
print('It is neutral for', '{:.1%}'.format(neu))

unique_string = (' ').join(reg_list)
wc = WordCloud(width=1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wc)
plt.axis('off')
plt.show()

