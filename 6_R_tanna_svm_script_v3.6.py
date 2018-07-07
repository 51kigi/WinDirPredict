#サンプルっぽい
#https://qiita.com/kazuki_hayakawa/items/18b7017da9a6f73eba77
#  http://www.turbare.net/transl/scipy-lecture-notes/packages/scikit-learn/index.html
#http://momijiame.tumblr.com/post/114751531866/python-iris-%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%E3%82%92%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E3%83%99%E3%82%AF%E3%82%BF%E3%83%BC%E3%83%9E%E3%82%B7%E3%83%B3%E3%81%A7%E5%88%86%E9%A1%9E%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B
#https://qiita.com/rennnosuke/items/fab837825b64bf50be56
#  SVM関連
#http://neuro-educator.com/ml3/
#https://algorithm.joho.info/machine-learning/python-scikit-learn-nyumon/
#https://blog.excite.co.jp/exdev/28958132/

#pandas
#https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E6%8A%BD%E5%87%BA
#https://pythondatascience.plavox.info/pandas/csv%e3%83%95%e3%82%a1%e3%82%a4%e3%83%ab%e3%81%ae%e8%aa%ad%e3%81%bf%e8%be%bc%e3%81%bf
# https://note.nkmk.me/python-pandas-read-csv-tsv/

#   以下は直接関係ないリンク
#http://d.hatena.ne.jp/n_shuyo/20100528/kernel_pca
#https://pepese.github.io/blog/python-ml-svm-multiclass/

#大きな流れ
#１、ファイルを読み込む
#２、結果と原因のデータセットに分ける
#３、学習する
#４、モデルを書き出す


import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn import svm
from sklearn import multiclass
from sklearn import metrics
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
#モデルの切り替え時
#from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.metrics import accuracy_score

dataset_org=pd.read_csv("./data/test_set_tanna3.5.csv")
X=dataset_org.iloc[:,0:6]
Y=dataset_org.iloc[:,6]

#データ分割
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=None)
#データ標準化
sc=StandardScaler()
sc.fit(X_train)
X_train_std=sc.transform(X_train)
X_test_std=sc.transform(X_test)
#学習
model=SVC(kernel='linear',random_state=None)
model.fit(X_train_std,Y_train)
#モデルの保存
filename='6_weather_predict_model_py_3.6'
pickle.dump(model,open(filename,'wb'))

#以下は精度テスト
loaded_model=pickle.load(open(filename,'rb'))
pred_train=loaded_model.predict(X_train_std)
accuracy_train=accuracy_score(Y_train,pred_train)
print('トレーニングデータに対する正解率　%.2f' % accuracy_train)

pred_test=loaded_model.predict(X_test_std)
accuracy_test=accuracy_score(Y_test,pred_test)
print('テストデータに対する正解率　:%.2' % accuracy_test)

