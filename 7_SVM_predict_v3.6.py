#v3.6対応
import numpy as np
import pandas as pd
import datetime
from sklearn import datasets
from sklearn import svm
from sklearn import multiclass
from sklearn import metrics
#from sklearn.cross_validation import train_test_split　　'depreciated
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
#from sklearn.grid_search import GridSearchCV 'depreciated
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
#モデルの切り替え時
from sklearn.linear_model import LogisticRegression
from sklearn.kernel_ridge import KernelRidge

import pickle
from sklearn.metrics import accuracy_score

print('process start')
d=datetime.datetime.today()
print('d:',d)

filename='./model/6_weather_predict_model_LR_py_3.6'
output_file_name='./result/7_SVM_result_py.csv'
for_pred_data_file_name='../test/7_input_for_predict_tanna.csv'
#後でこちらのフォルダに切り替える（データ収集スクリプトの修正をしてから）
#for_pred_data_file_name='./data/7_input_for_predict_tanna.csv'

#モデルをファイルから読み出す
loaded_model=pickle.load(open(filename,'rb'))

print('predict start')
d=datetime.datetime.today()
print('d:',d)

#予測対象データを読み出す
for_pred_data=pd.read_csv(for_pred_data_file_name)
#データの整形
X=for_pred_data.iloc[:,0:6]
print('X')
#予測実施
pred_result=loaded_model.predict(X)
print(pred_result)

print('predict end')
d=datetime.datetime.today()
print('d:',d)

result_df=pd.DataFrame([d,X,pred_result],)
result_df.to_csv(output_file_name)
