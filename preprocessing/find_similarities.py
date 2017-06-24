import dill as pickle
import re
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer
import gensim
lem = WordNetLemmatizer()

data = pickle.load(open('p_data_vec.p', 'rb'))
print('Data loaded.')

print(len(data))

model = gensim.models.KeyedVectors.load_word2vec_format('../../data/GoogleNews-vectors-negative300.bin', binary=True)
print('Model loaded.')

def preproc_query(q):
    q = q.lower()
    q = re.sub('"', '', q)
    q = re.sub("'", '', q)
    q = re.sub('\n', '', q)
    q = re.sub('\t', '', q)
    q = re.sub('\\\\', '', q)

    for wi, w in enumerate(q.split()):
        q.split()[wi] = lem.lemmatize(w)

    return q

def sent2vec(sent):
    """ converts a sentence into a vector """
    sent_vec = np.ones(300)
    for w in sent.split():
        if w in model:
            sent_vec *= model[w]

    return sent_vec

top                 = 10
most_similar        = [[0,0]]  * top
most_similar_scores = [-1] * top

queries = [
"Miley Cyrus Obsessed Fan Sneaks Into Singer’s Dressing Room And Leaves",
"Lindsay Lohan to sign USD one million deal with Harper Collins",
"Miley Cyrus is into unicorns",
"Common featured on Game of Thrones The Mixtape",
"In SXSW Conversation Edward Snowden Calls For Better Security Standards",
"Juan Pablo Galavis Who is he and why should you care"
]

for q in queries:
    q = preproc_query(q)
    qv = sent2vec(q)

    def cos_sim(a, b):
        return np.cos(np.dot(a,b) / (np.sqrt(np.sum(a**2)) * np.sqrt(np.sum(b**2))))


    for i in list(data.keys()):
        for si, sv in enumerate(data[i]['p_sentences_vec']):
            score = cos_sim(qv, sv)

            # check for duplicate sentences
            poss_candidate = True
            for (ms_i, ms_si) in most_similar:
                if data[i]['p_sentences'][si] == data[ms_i]['p_sentences'][ms_si]:
                    poss_candidate = False

            if score > min(most_similar_scores) and poss_candidate:

                score_to_replace_id = most_similar_scores.index(min(most_similar_scores))
                most_similar[score_to_replace_id] = [i, si]
                most_similar_scores[score_to_replace_id] = score


    print("Query: %s" %(q))
    print("Most Similar Sentences in Data:")
    for i, ms in enumerate(most_similar):
        data_id = ms[0]
        sent_id = ms[1]
        print("#%02d: %s \t Score: %f, Datapoint: %i, Sentence: %i" %(i, data[data_id]['sentences'][sent_id], most_similar_scores[i], data_id, sent_id))
