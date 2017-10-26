#
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec


import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



documents = [
    'eat apple',
    'eat orange',
    'eat rice',
    'drink juice',
    'orange juice',
    'apple juice',
    'drink milk',
    'drink water'
]


#

from nltk.tokenize import sent_tokenize, word_tokenize
documents_tokenized = [word_tokenize(document) for document in documents]


# In[5]:
#


class LabeledLineSentence(object):
    def __init__(self, texts, idxlist):
        self.texts = texts
        self.doc_list = idxlist

    def __iter__(self):
        for idx, text in zip(self.doc_list, self.texts):
            wtok = text
            tags = [idx]

            yield TaggedDocument(words=wtok, tags=tags)

#

tagged_documents_iterator = LabeledLineSentence(documents_tokenized, range(len(documents_tokenized)) )


#
list(tagged_documents_iterator)

#

model = Doc2Vec(size=500, window=10,  workers=11, alpha=0.025, min_alpha=0.025, iter=10, min_count=1)

#

model.build_vocab(tagged_documents_iterator)


# In[12]:


model.wv


# In[13]:


model.train(tagged_documents_iterator, total_examples=model.corpus_count, epochs=model.iter)


# In[ ]:


keyedVector = model.wv


# In[ ]:


keyedVector.most_similar(positive=['orange'])
