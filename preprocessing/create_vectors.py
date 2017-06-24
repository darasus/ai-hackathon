import dill as pickle
import gensim
import numpy as np

p_data = pickle.load(open('p_data.p','rb'))
print('Data read. Containing %i datapoints.' %(len(p_data)))

model = gensim.models.KeyedVectors.load_word2vec_format('../../data/GoogleNews-vectors-negative300.bin', binary=True)
print('Model loaded.')

def sent2vec(sent):
    """ converts a sentence into a vector """
    sent_vec = np.ones(300)
    for w in sent.split():
        if w in model:
            sent_vec *= model[w]

    return sent_vec


for i in list(p_data.keys()):
    n_sentences = len(p_data[i]['p_sentences'])
    p_data[i]['p_sentences_vec'] = list()
    for sent in p_data[i]['p_sentences']:
        p_data[i]['p_sentences_vec'].append(sent2vec(sent))

pickle.dump(p_data, open('p_data_vec.p', 'wb'))

print('Data saved.')
