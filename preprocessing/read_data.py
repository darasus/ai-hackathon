import csv
import requests
from collections import defaultdict
from readability import Document
from bs4 import BeautifulSoup
import dill as pickle
from time import time
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import re

lem = WordNetLemmatizer()

### Read in data
data_path = '../../data/newsCorpora.csv'

data = defaultdict(dict)

with open(data_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    i = 0
    for row in csv_reader:
        if row[4] == 'e':
            assert len(row) == 8, "Datapoint %i has length %i, expected 8" %(i, len(row))

            data[i]['id']           = row[0]
            data[i]['title']        = row[1]
            data[i]['url']          = row[2]
            data[i]['publisher']    = row[3]
            data[i]['category']     = row[4]
            data[i]['story']        = row[5]
            data[i]['hostname']     = row[6]
            data[i]['timestamp']    = row[7]

        i += 1

cats = set()

for ci in list(data.keys()):
    cats.add(data[ci]['category'])

print("Categories", cats)


print('Data read. %i dataopints.' %(len(data)))

### get the text
s = time()
n = 0
p_data = defaultdict(dict)

for i in list(data.keys()):

    while n < 1000:

        if data[i]['category'] == 'e': # only use entertainment articles

            # logging
            if n % 10 == 0 and n != 0:
                print("10 more datapoints processed. Total %i. Time: %.2f" %(n, time()-s))
                s = time()

            # get text from url
            try:
                r = requests.get(url=data[i]['url'])
                doc = Document(r.text)
                summary = doc.summary()
            except:
                print("Skipped datapoint %i" %(i))
                continue

            # process text
            soup = BeautifulSoup(summary, 'html.parser')
            text = soup.get_text()
            text = text.lower()
            text = re.sub('"', '', text)
            text = re.sub("'", '', text)
            text = re.sub(",", '', text)
            text = re.sub(":", '', text)
            text = re.sub(";", '', text)
            text = re.sub("-", '', text)
            text = re.sub("#", '', text)
            text = re.sub("@", '', text)
            text = re.sub("%", '', text)
            text = re.sub("$", '', text)
            text = re.sub("§", '', text)
            text = re.sub("&", ' and ', text)
            text = re.sub("/", ' and ', text)
            text = re.sub("=", ' and ', text)
            text = re.sub("`", ' and ', text)
            text = re.sub("´", ' and ', text)

            text = re.sub('\n', '', text)
            text = re.sub('\t', '', text)
            text = re.sub('\\\\', '', text)

            p_data[n]['id']             = data[i]['id']
            p_data[n]['title']          = data[n]['title']
            p_data[n]['url']            = data[n]['url']
            p_data[n]['publisher']      = data[n]['publisher']
            p_data[n]['category']       = data[n]['category']
            p_data[n]['story']          = data[n]['story']
            p_data[n]['hostname']       = data[n]['hostname']
            p_data[n]['timestamp']      = data[n]['timestamp'] 
            p_data[n]['text']           = text
            p_data[n]['sentences']      = sent_tokenize(p_data[n]['text'])
            p_data[n]['p_sentences']    = sent_tokenize(p_data[n]['text'])

            for si, sent in enumerate(p_data[n]['sentences'] ):
                for wi, w in enumerate(sent.split()):
                    p_data[n]['p_sentences'][si].split()[wi] = lem.lemmatize(w)

            n += 1

print("%i datapoints created." %(len(p_data)))

pickle.dump(p_data, open('p_data.p', 'wb'))

print('Data saved.')
