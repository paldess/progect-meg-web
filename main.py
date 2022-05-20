from flask import Flask, jsonify, request, json
from flask_cors import CORS
import numpy as np
import pandas as pd
import dill
from tqdm import tqdm
import os, sys
from logzero import logger, logfile
import statistics
from scipy.stats import iqr
import json
from datetime import datetime, date 
import pickle
import time

from megafon.save_file_param import open_json
param_json = open_json()

from sklearn.metrics import f1_score

logfile('my_logfile.log')

import mysql.connector



app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    with open('/var/www/html/model/model.dill', 'rb') as f:
        model = dill.load(f)
        logger.info('модель загружена')
    
    dict_w = request.get_json(force=True)
    df = pd.DataFrame()
    df['text'] = [dict_w['text']]
    threshold = 0.5036
    result_proba = model.predict_proba(df)[:,1][0]
    result = [1 if result_proba > threshold else 0][0]
    if result == 1:
        out = [result, round((result_proba - threshold) * 2 * 100, 2)]
    else:
        out = [result, round((threshold - result_proba) * 2 * 100, 2)]
    model = None
    return jsonify(out)

@app.route('/predict_megafon', methods=['POST'])
def predict_megafon():
    with open('/var/www/html/megafon/model_pca_dill.pkl', 'rb') as f:
        model = dill.load(f)
        logger.info('модель загружена')
    dict_w = request.get_json(force=True)
    for i in dict_w:
        for j in dict_w[i].split('-'):
            if not j.isnumeric():
                return  jsonify([0, 'Неверные данные!', 'Только цифры'])
        if i == 'id':
            if int(dict_w[i])<0:
                return  jsonify([0, 'Неверные данные!', 'ID пользователя неверен'])
        elif i == 'time':
            x = dict_w[i].split('-')
            if int(x[0])<2015 or int(x[0])>2022 or int(x[1])<1 or int(x[1])>12 or int(x[2])<1 or int(x[2])>31:
                return  jsonify([0, 'Неверные данные!', 'Дата неверна'])
        elif i == 'service':
            if not int(dict_w[i]) in [1,2,4,5,6,7,8,9]:
                return  jsonify([0, 'Неверные данные!', 'Не из списка услуга'])    

    con = mysql.connector.connect(host='localhost', user='web_user', password='1111', db='megafon')
    sql = f"select * from features where id = {dict_w['id']}"
    data_features = pd.read_sql(sql, con)
    if data_features.shape[0] == 0:
        return jsonify([0, 'Нет такого пользователя', 0])
    data_features.drop('index', axis=1, inplace=True)
    time_to_date_time = dict_w['time'].split('-')
    my_datetime = date(int(time_to_date_time[0]), int(time_to_date_time[1]), int(time_to_date_time[2]))
    time_1 = time.mktime(my_datetime.timetuple())
    try:
        data_test = pd.DataFrame(np.array([[0,], [int(dict_w['id']),], [int(dict_w['service']),], [int(time_1),]]).T, 
            columns=['Unnamed: 0', 'id', 'vas_id', 'buy_time'])
    except:
        return jsonify([0, 'Не все поля заполнены', 0])
    data = pd.merge_asof(data_test, data_features, on='buy_time', by='id', direction='nearest')
    y_pred = model.predict_proba(data)[:,1][0]
    if y_pred >= param_json['xgb_pca']:
        pred = 1
    else:
        pred = 0
    
    from megafon.predict_megafon import predict_megafon
    out = predict_megafon(data, param_json, model)
    out = [int(i) for i in out.loc[0][1:]]

    model = None
    return jsonify({0: f'{pred}/{int(round(y_pred, 2)*100)}%', 1: out[0], 2: out})

@app.route('/hello', methods=['GET'])
def hello():
    logger.info('привет космонавтам!')
    a = jsonify('test connect!')
    return a

#
#

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
