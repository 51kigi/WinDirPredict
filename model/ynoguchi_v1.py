#野口モデルの実装
#コマンドライン引数で予測用の数値の入ったCSVファイルを指定
#１、CSVからモデルに入れる値を取得
#２、モデルで使用するw1,w2を指定されたファイルから取得
#３、計算
#４、結果をもとの数値に戻して（二桁の風速、風向を意味する値）CSV出力

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
#要素をループしてマイナスなら0に置き換え
b2=b1.dot(w2_df.values)
print(b2)
b3=b2.dot(w3_df.values)
print(b3)
#10, 12, 14, 16, 20, 22, 24, 26 を順番に 0,1,2,3,4,5,6,7 に置き換え。（8パターンの分類問題）
#最大確立のラベルが予想値
#整えてCSV出力