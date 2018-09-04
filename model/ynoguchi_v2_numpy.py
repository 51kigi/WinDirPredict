#野口モデルの実装
#コマンドライン引数で予測用の数値の入ったCSVファイルを指定
#１、CSVからモデルに入れる値を取得
#２、モデルで使用するw1,w2を指定されたファイルから取得
#３、計算
#４、結果をもとの数値に戻して（二桁の風速、風向を意味する値）CSV出力

#pandasなしで実施（AzureでPandasが使えないので、、）

#ref
#https://qiita.com/tanemaki/items/2ed05e258ef4c9e6caac
#http://www.mwsoft.jp/programming/numpy/csv.html
#https://deepage.net/features/numpy-loadsavetxt.html
#https://note.nkmk.me/python-numpy-where/
#http://clc.gonna.jp/2017/04/post-1490/



w1_path='./w1.csv'
w2_path='./w2.csv'
w3_path='./w3.csv'
b1_path='./b1.csv'
b2_path='./b2.csv'
b3_path='./b3.csv'
output_path='../pred/ynoguchi_pred_not_pandas.csv'
input_path='../pred/7_input_for_predict_tanna.csv'

import sys
import numpy as np
import matplotlib.pyplot as plt

#入力数値を取得するファイルパス
input_df=np.loadtxt(input_path,delimiter=",",skiprows=1)
print(input_df)
#中間層を軒並み読み込む

w1_df=np.loadtxt(w1_path,delimiter=",")
w2_df=np.loadtxt(w2_path,delimiter=",")
w3_df=np.loadtxt(w3_path,delimiter=",")
b1_df=np.loadtxt(b1_path,delimiter=',')
b2_df=np.loadtxt(b2_path,delimiter=',')
b3_df=np.loadtxt(b3_path,delimiter=',')
print('w1')
print(w1_df)
print('w2')
print(w2_df)
print('w3')
print(w3_df)
print('b1')
print(b1_df)
print('b2')
print(b2_df)
print('b3')
print(b3_df)

#読み込み時にヘッダーを飛ばしたのでそのままでよい
input_df2=input_df
print('input data')
print(input_df2)
#行列計算
b1=input_df2.dot(w1_df)+b1_df
print('first calc')
print(b1)
#各要素について負であれば0に置き換える。npで一気に処理
b1_cln=np.where(b1<0,0,b1)
print('b1 first calc cleaned')
print(b1_cln)
#もう一回行列計算
b2=b1_cln.dot(w2_df)+b2_df
print('b2 second calc')
print(b2)
b2_cln=np.where(b2<0,0,b2)
print('second calc cleaned')
print(b2_cln)
#最後の行列計算
b3=b2_cln.dot(w3_df)+b3_df
print('b3 third calc')
print(b3)

def softmax(arglst):
    c=np.max(arglst)
    exp_a= np.exp(arglst - c)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y

res_softmax=softmax(b3)

x=np.arange(0,8,1)
x_name=('North','East','South','West','StrongN','StrongE','StrongS','StrongW')
#plt.plot(x_name,b3)

plt.bar(x_name,res_softmax)

#保存したかったらshowしてはいけない
#plt.show()

print('max')
plt.savefig('ynmodel.png')

#Maxを取る
print(np.argmax(res_softmax))
tmp_pred=np.argmax(res_softmax)

if tmp_pred==0:
    pred=10
elif tmp_pred==1:
    pred=12
elif tmp_pred==2:
    pred=14
elif tmp_pred==3:
    pred=16
elif tmp_pred==4:
    pred=20
elif tmp_pred==5:
    pred=22
elif tmp_pred==6:
    pred=24
elif tmp_pred==7:
    pred=26
else:
    pred=99
print('result')
print(pred)


#10, 12, 14, 16, 20, 22, 24, 26 を順番に 0,1,2,3,4,5,6,7 に置き換え。（8パターンの分類問題）
#最大確立のラベルが予想値
#整えてCSV出力