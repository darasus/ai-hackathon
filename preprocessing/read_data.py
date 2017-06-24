import csv
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
import re



### Read in data
data_path = '../data/newsCorpora.csv'

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

### Build Vocablurary
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


vocab = set()
for i in list(data.keys())[1:10]:
    print(data[i]['url'])
    print(data[i]['title'])

    # build request
    r = requests.get(url=data[i]['url'])
    soup = BeautifulSoup(r.text, 'html.parser')
    text = BeautifulSoup.get_text()
    print(text)
