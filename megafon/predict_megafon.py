#!/usr/bin/env python
# coding: utf-8

# In[1]:


# импорт необходимых элементов
import statistics
from scipy.stats import iqr
import json
from datetime import datetime


import pandas as pd
import numpy as np
import dask.dataframe as dd
from sklearn.metrics import f1_score



def predict_megafon(data, param_json, model):
    df = pd.DataFrame()
    for i in param_json['uslugi']:
        data['vas_id'] = i
        df[i] = model.predict_proba(data)[:, 1]
    recomendate = pd.DataFrame()
    recomendate['id'] = data['id']
    recomendate_sorted = pd.DataFrame(columns=[1,2,3,4,5,6,7,8])
    for i in df.index:
        a = pd.DataFrame()
        a['0'] = df.loc[i]
        recomendate_sorted.loc[recomendate_sorted.shape[0]] = a.sort_values('0', ascending=False).index
    for i in recomendate_sorted.columns:
        recomendate[i] = recomendate_sorted[i]
    return recomendate


# In[ ]:




