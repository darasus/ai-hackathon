import csv
import requests
from collections import defaultdict
from readability import Document
from bs4 import BeautifulSoup
import dill as pickle
from time import time



### Read in data
data_path = '../../data/newsCorpora.csv'

data = defaultdict(dict)
with open(data_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='\t')
    i = 0
    for row in csv_reader:
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

print('Data read. %i dataopints.' %(len(data)))
data2 = defaultdict(dict)
### get the text
s = time()
for i in list(data.keys())[:1000]:

    # logging
    if i % 100 == 0 and i != 0:
        print("100 datapoints processed. Time: %.2f" %(time()-s))
        s = time()

    # get text from url
    try:
        r = requests.get(url=data[i]['url'])
        doc = Document(r.text)
        summary = doc.summary()
    except:
        continue

    soup = BeautifulSoup(summary, 'html.parser')
    text = soup.get_text()


    data2[i] = data[i]
    data2[i]['text'] = text



pickle.dump(data, open('data2.p','wb'))
