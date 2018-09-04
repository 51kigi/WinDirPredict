#アメダスデータを取り出すときのpythonコード
#http://qiita.com/kitsuyui/items/4906bb457af4d0e2d0a5
#http://qiita.com/mojaie/items/241eb7006978e6962d05
#http://www.kisse-logs.com/2017/09/18/python-pandas-dataframe-dropna/
#https://pythondatascience.plavox.info/pandas/%e3%83%87%e3%83%bc%e3%82%bf%e3%83%95%e3%83%ac%e3%83%bc%e3%83%a0%e3%82%92%e5%87%ba%e5%8a%9b%e3%81%99%e3%82%8b
#https://pythondatascience.plavox.info/pandas/%e8%a1%8c%e3%83%bb%e5%88%97%e3%82%92%e5%89%8a%e9%99%a4
#https://note.nkmk.me/python-pandas-dataframe-rename/
#https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E6%8A%BD%E5%87%BA
#https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E9%95%B7%E3%81%95%E3%82%92%E7%A2%BA%E8%AA%8D
#https://pythondatascience.plavox.info/pandas/%E3%83%87%E3%83%BC%E3%82%BF%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%82%92%E5%87%BA%E5%8A%9B%E3%81%99%E3%82%8B


import pandas
import json
import urllib.request
import csv
import datetime

url_mishima='http://www.jma.go.jp/jp/amedas_h/today-50206.html?areaCode=000&groupCode=35'  #三島
url_aziro='http://www.jma.go.jp/jp/amedas_h/today-50281.html?areaCode=000&groupCode=35' #網代

#WebからAmedasデータを取得
fetched_mishima=pandas.io.html.read_html(url_mishima,header=0)
fetched_aziro=pandas.io.html.read_html(url_aziro,header=0)

#取得したデータフレームにヘッダーを設定
fetched_mishima[5].columns=['hour','Temp','Rain','WinDir','WinSpd','Sun','Humid','Press']
fetched_aziro[5].columns=['hour','Temp','Rain','WinDir','WinSpd','Sun','Humid','Press']

#邪魔な1行目を削除
cls1_mishima=fetched_mishima[5].drop(0)
cls1_aziro=fetched_aziro[5].drop(0)

#print(cls1_aziro)

#邪魔な列を削除(ファイルに出力した場合に付加される列)
#cls2_mishima=cls1_mishima.drop("Unnamed: 0",axis=1)
#cls2_aziro=cls1_aziro.drop("Unnamed: 0",axis=1)

#日照時間を削除
cls3_mishima=cls1_mishima.drop('Sun',axis=1)
cls3_aziro=cls1_aziro.drop('Sun',axis=1)

#NAがあるデータを削除
cls4_mishima=cls3_mishima.dropna(axis=0,how='any')
cls4_aziro=cls3_aziro.dropna(axis=0,how='any')

#蓄積用ファイルを出力しておく
cls4_mishima.to_csv("cls4_mishima.csv",encoding='utf-8',index=False)
cls4_aziro.to_csv("cls4_aziro.csv",encoding='utf-8',index=False)

#print(cls4_mishima)
#print(cls4_aziro)

lennum_aziro=len(cls4_aziro.index)
lennum_mishima=len(cls4_mishima.index)

colnum_aziro=len(cls4_aziro.columns)
colnum_mishima=len(cls4_mishima.columns)

#print(lennum_aziro)
#print(lennum_mishima)
#print(colnum_aziro)
#print(colnum_mishima)
#print(cls4_aziro.shape)
#print(cls4_mishima.iloc[lennum_mishima-1])

WindDirDict={
    "北":0,"北北東":22.5,"北東":45,"東北東":67.5,"東":90,
    "東南東":112.5,"南東":135,"南南東":157.5,"南":180,
    "南南西":202.5,"南西":225,"西南西":247.5,"西":270,
    "西北西":292.5,"北西":315,"北北西":337.5,"静穏":0
}

#作成したモデルから3時間後の状態を得るための直近の状況ファイルを作る
#mishima_dir,mishima_speed,aziro_dir,aziro_speed,tannna_dir,tanna_speed,judg
#三島データセットの3,4番目、網代データセットの3,4番目を取得

mishima_dir=cls4_mishima.iloc[lennum_mishima-1,3]
mishima_spd=cls4_mishima.iloc[lennum_mishima-1,4]
aziro_dir=cls4_aziro.iloc[lennum_aziro-1,3]
aziro_spd=cls4_aziro.iloc[lennum_aziro-1,4]
print(mishima_dir,mishima_spd,aziro_dir,aziro_spd,sep=",")
print(WindDirDict[mishima_dir],mishima_spd,WindDirDict[aziro_dir],aziro_spd,sep=",")

#丹那のデータを読み込む
#サイトアドレスを外だし
tanna_url_filepath='./tanna_wind_url.txt'
with open(tanna_url_filepath) as f:
  s=f.read()
  print(type(s))
tanna_url_parent=s
print(tanna_url_parent)
todayObj=datetime.date.today()
today_url=str(todayObj.year) + str(todayObj.month).zfill(2) + str(todayObj.day).zfill(2)

url_tanna=tanna_url_parent + today_url
print(url_tanna)
res_tanna=urllib.request.urlopen(url_tanna)
#areaが日本語なので文字化けするのを回避するためコーディングを指定
res2_tanna=res_tanna.read().decode('shift-jis')

json_tanna_data=json.loads(res2_tanna)

#print('webapi')
#print(res2_tanna)
#print('json')
#print(json_tanna_data)
#print('dict')
#print('json_dict:{}'.format(type(json_tanna_data)))
#print('recode type')
#print(type(json_tanna_data['recode']))

#JSONで取得した丹那データのレコード部分はなぜかリストで格納されている
tanna_data_list=json_tanna_data['recode']
#print('list')
#print(tanna_data_list)
#print('element')
print(tanna_data_list[len(tanna_data_list)-1])
#リストの要素は辞書型になっている
print(tanna_data_list[len(tanna_data_list)-1].keys())
#keyは'no', 'unix', 'max', 'min', 'avg', 'direc', 'vcc', 'temp', 'humi'
#ここから風向と風速を取得する
#元データは255までで360度を表現している
print('winddir')
tanna_windir=round(tanna_data_list[len(tanna_data_list)-1]['direc']*360/255,1)
print(tanna_windir)
#元データは数値が10倍されているが、アメダス側をそれに合わせる（教師データもそうなってる）
print('windspd')
tanna_windspd=tanna_data_list[len(tanna_data_list)-1]['avg']
print(tanna_windspd)

print(WindDirDict[mishima_dir],mishima_spd,WindDirDict[aziro_dir],aziro_spd,tanna_windir,tanna_windspd,sep=",")
print(WindDirDict[mishima_dir],float(mishima_spd)*10,WindDirDict[aziro_dir],float(aziro_spd)*10,tanna_windir,tanna_windspd,sep=",")

file_out=open('C:/Users/gk/Documents/test/7_input_for_predict_tanna.csv','w')
file_out.write('mishima_dir,mishima_speed,aziro_dir,aziro_speed,tannna_dir,tanna_speed,judg\n')

file_out=open('C:/Users/gk/Documents/test/7_input_for_predict_tanna.csv','a')
file_out.write(str(WindDirDict[mishima_dir]) + ',' + str(float(mishima_spd)*10) \
  + ',' +str(WindDirDict[aziro_dir]) + ',' + str(float(aziro_spd)*10) \
  + ',' + str(tanna_windir) + ',' + str(tanna_windspd) + '\n')

#北　0
#北東　45
#東　90
#南東　135
#南　180
#南西　225
#西　270
#北西　315
#
#丹那方角
#北	255
#北北東	15.9375
#北東	31.875
#東北東	47.8125
#東	63.75
#東南東	79.6875
#南東	95.625
#南南東	111.5625
#南	127.5
#南南西	143.4375
#南西	159.375
#西南西	175.3125
#西	191.25
#西北西	207.1875
#北西	223.125
#北北西	239.0625


