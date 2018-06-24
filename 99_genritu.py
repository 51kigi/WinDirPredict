import pandas
import urllib.request
fetched_genritu=pandas.io.html.read_html('http://www.sunny-spot.net/sis/sky/index.html?area=5&location_id=0024')
print (fetched_genritu[0])
fetched_genritu[0].to_csv('C:/Users/gk/OneDrive/文書/Projects/para/WindPredictMachineLearning/1_amedas data/test_genritu.csv')
gap_height=int(fetched_genritu[0].iloc[3,9]) - int(fetched_genritu[0].iloc[8,9])
print (gap_height/100)
gap_tmp=int(fetched_genritu[0].iloc[6,9]) - int(fetched_genritu[0].iloc[11,9])
print(gap_tmp)
print(gap_tmp/(gap_height/100))

#１、天地入れ替え
#２、不要列削除
#３、列ラベルリネーム
#４、気温減率計算
#５、ターミナル出力
#６、ファイル出力