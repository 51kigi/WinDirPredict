#http://pgt.hatenablog.jp/entry/2014/08/07/002914
#coding:utf-8

from sklearn import svm
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import csv

f = open('C:/Users/k/Documents/WinDirPredict/SVM.csv', 'r')
data = []
c = csv.reader(f)  # CSV読み込み用オブジェクトの生成
for row in c:
    data.append(row)   #spamデータをリスト型のdataに格納
f.close()

# dataの個数は4601個で属性のベクトルは58次元.58個目の要素が判別値.ex).data[1][58] = spam
# 1~1813:spam 1を返す ,1814~4601:nonspam 0を返す

num = len(data)       #4602
for i in range(1,num):
    if data[i][58] == 'spam':
        data[i][58] = 1          #負例、正例の値を振り分ける
    else:
        data[i][58] = 0

for i in range(num):            #idを削除する
    data[i].pop(0)


#まずは適当にデータを分割してSVMによる判定を行う。

x = []
y = []
one = 1
zero = 0

for i in range(1,907):     #正例の教師値
    x.append(data[i])

for i in range(1814,3207): #負例の教師値
    x.append(data[i])

teach_num = len(x)     #2209

for i in range(teach_num):   #クラスレベル
    if i < 906:
        y.append(one)
    else:
        y.append(zero)

test_data = []
answer_data = []

for i in range(907,1813):     #正例の教師値
    test_data.append(data[i])

for i in range(3207,4602): #負例の教師値
    test_data.append(data[i])

test_num = len(test_data)

for i in range(test_num):   #クラスレベル
    if i < 906:
        answer_data.append(one)
    else:
        answer_data.append(zero)

pre_list = []
pre_num = len(test_data)
num_answer = 0

clf = svm.SVC(kernel='rbf') #Support Vector Classification,RBFカーネルを使用
clf.fit(x,y) #学習
pre_list = clf.predict(test_data) #予測

for i in range(pre_num):
    if answer_data[i] == pre_list[i]:
        num_answer += 1

#print confusion_matrix(answer_data,pre_list)   #分類結果を表示する

accuracy = (num_answer*1.0/pre_num)*100
#print accuracy

target_names = ['class0', 'class1']
print (classification_report(answer_data,pre_list,target_names=target_names)) 