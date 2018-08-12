#野口モデルの実装
#コマンドライン引数で予測用の数値の入ったCSVファイルを指定
#１、CSVからモデルに入れる値を取得
#２、モデルで使用するw1,w2を指定されたファイルから取得
#３、計算
#４、結果をもとの数値に戻して（二桁の風速、風向を意味する値）CSV出力

#ref
#https://qiita.com/tanemaki/items/2ed05e258ef4c9e6caac


w1_path='./w1.csv'
w2_path='./w2.csv'
w3_path='./w3.csv'
output_path='../pred/ynoguchi_pred.csv'
input_path='../pred/7_input_for_predict_tanna.csv'

import sys
import numpy as numpy
import pandas as pd

#面倒なので引数にファイルパスを渡すのはやめる
#argvs=sys.argv
#argc=len(argvs)

#print (argvs)
#print (argc)
#print(argvs[1])

#入力数値を取得するファイルパス
input_df=pd.read_csv(input_path,sep=',')
print(input_df)
#中間層を軒並み読み込む
w1_df = pd.read_csv(w1_path,sep=',',header=None)
w2_df=pd.read_csv(w2_path,sep=',',header=None)
w3_df=pd.read_csv(w3_path,sep=',',header=None)
print(w1_df)
print(w2_df)
print(w3_df)

#余計な要素を除外する
input_df2=input_df.iloc[:,0:6]
print(input_df2)
#各要素について負であれば0に置き換える
b1=input_df2.dot(w1_df.values)
print(b1)

#pandasのdataframe上で処理
#0以下の値をすべてNaNにする
b1_no0=b1[b1>0]
#NaNを0埋めする
b1_mod=b1_no0.fillna(0)
print(b1_mod)

#要素をループしてマイナスなら0に置き換え
b2=b1_mod.dot(w2_df.values)
print(b2)
b2_no0=b2[b2>0]
b2_mod=b2_no0.fillna(0)
print(b2_mod)

b3=b2_mod.dot(w3_df.values)
print(b3)
print('max')
#最大値を求めるため、天地を逆にしてMaxを取る
b3_T=b3.T
print(b3_T)
print(b3_T[0].max())
#最大値を持つインデックスを取得
print(b3_T[0].idxmax())
tmp_pred=b3_T[0].idxmax()
if tmp_pred==0:
    pred=10
if tmp_pred==1:
    pred=12
if tmp_pred==2:
    pred=14
if tmp_pred==3:
    pred=16
if tmp_pred==4:
    pred=20
if tmp_pred==5:
    pred=22
if tmp_pred==6:
    pred=24
if tmp_pred==7:
    pred=26
else:
    pred=99
print(pred)


#10, 12, 14, 16, 20, 22, 24, 26 を順番に 0,1,2,3,4,5,6,7 に置き換え。（8パターンの分類問題）
#最大確立のラベルが予想値
#整えてCSV出力