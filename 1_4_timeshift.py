#integratedファイルから丹那を任意の時間分ずらしたファイルを作成する
import pandas as pd
import datetime

#1,ファイルを読み込む
#2,丹那分を切り出して別のデータフレームに
#3,別のデータフレームの日付部分に対して3時間前の時間を横につける（この時間にから見て、該当行の値は3時間後になる）
#4,別データフレームのヘッダーを3時間ずらしであることがわかるように変更する
#4,3で付けた時間をキーに元のデータフレームと結合する
#5,ファイル出力！

#1
df=pd.read_csv('./data/raw/3_integrated/integrated_test.csv')

#2
df_tanna=df.iloc[:,[0,1,2,3,4,5,6,7]]

#特定の行をStringに
df_tanna['date_tanna'].astype(str)
#dataframeで見るとobject型（Series)
df_tanna.dtypes
#Objectの中はStringで埋まっている
type(df_tanna['date_tanna'][0])


test_date=df_tanna.loc[1:1,'date_tanna']
print(str(test_date.size))
print(str(test_date.values))
# datetime.datetime.strptime(str(test_date),'%Y/%m/%d %H:%M:%S')