#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import ast
import warnings
warnings.filterwarnings('ignore')


# In[2]:


from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve, roc_curve, f1_score


# In[3]:


# from google.colab import drive
# drive.mount("/content/drive")


# In[4]:


data_read = pd.read_csv('fake_or_real_news.csv', index_col=0)
data_read['label'] = [1 if i == 'FAKE' else 0 for i in data_read['label']]
data_read.head()


# In[5]:


from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
import string
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk 
nltk.download('stopwords')
from pymorphy2 import MorphAnalyzer
from tqdm import tqdm
import re
from sklearn.feature_extraction.text import TfidfVectorizer


class preds(BaseEstimator, TransformerMixin):
  def __init__(self, column):
    self.column = column
    self.stopwords = stopwords.words('english')
    self.morph_analizer = MorphAnalyzer()
    pattern = r'[\d.,]+|[A-Z][.A-Z]+\b\.*|\w+|\S'
    self.tokenizer = RegexpTokenizer(pattern)

  def fit(self, x, y=None):
    return self

  def transform(self, x, y=None):
    data = x[self.column].copy()
    for i in tqdm(list(data.index)):
      data.loc[i] = ' '.join([self.morph_analizer.parse(j)[0].normal_form for j in self.tokenizer.tokenize(data.loc[i]) if j not in self.stopwords and len(j) > 2])
    return data

pip = Pipeline([('transfom', preds('text')), 
                ('tfidf', TfidfVectorizer(max_features=5000)),
                ('LR', LogisticRegression())])

# pip[:2].fit(data_read, data_read['label'])


# In[6]:


x_train, x_test, y_train, y_test = train_test_split(data_read, data_read['label'], test_size=0.3, random_state=5)


# In[ ]:


pip.fit(x_train, y_train)


# In[ ]:


y_pred = pip.predict_proba(x_test)
p, r, th = precision_recall_curve(y_test, y_pred[:,1])
x = 2 * p * r / (p + r)
threshold = th[np.argmax(x)]
f1_score(y_test, [1 if i > threshold else 0 for i in y_pred[:,1]]), threshold


# In[ ]:


import dill

with open('model.dill', 'wb') as f:
  dill.dump(pip, f)
f.close()


# In[ ]:


with open('model.dill', 'rb') as f:
  pip_load = dill.load(f)


# In[ ]:


f.close()


# In[ ]:


pdf = pd.DataFrame()
pdf['text'] = [(data_read['text'].iloc[2])]
preds = pip_load.predict(pdf)
print(preds)


# In[ ]:




