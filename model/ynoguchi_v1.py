#野口モデルの実装
#コマンドライン引数で予測用の数値の入ったCSVファイルを指定
#１、CSVからモデルに入れる値を取得
#２、モデルで使用するw1,w2を指定されたファイルから取得
#３、計算
#４、結果をもとの数値に戻して（二桁の風速、風向を意味する値）CSV出力

w1_path='./w1.csv'
w2_path='./w2.csv'
w3_path='./w3.csv'
output_path='./ynoguchi_pred.csv'

import sys
import numpy as numpy
import pandas as import pd

argvs=sys.argv
argc=len(argvs)

print (argvs)
print (argc)
print(argvs[1])

#入力数値を取得するファイルパス
input_df=pd.read_csv(argvs[1],sep=',',header=None)
#中間層を軒並み読み込む
w1_df = pd.read_csv(w1_path,sep=',',header=None)
w2_df=pd.read_csv(w2_path,sep=',',header=None)
w3_df=pd.read_csv(w2_path,sep=',',header=None)

