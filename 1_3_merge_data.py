#丹那データとアメダスデータを結合する
import pandas as pd
import glob

tanna_cleaned_file_path='./data/raw/1_tanna/01_tannna_cleaned.csv'
amedas_cleaned_folder_path='./data/raw/2_amedas'
strOutputFile='./data/raw/3_integrated'

#丹那データをデータフレームに格納
df_tanna=pd
df_tanna=pd.read_csv(tanna_cleaned_file_path)

#アメダスフォルダからcleanedのファイルだを取得したリストを作る
amedas_file_list=glob.glob(amedas_cleaned_folder_path + '\*cleaned*')

print(amedas_file_list)

#リストのインデックスは整数でなければならないので辞書型の中にリストを入れ込む
df_amedas={}
for name in amedas_file_list:
    df_amedas[name]=pd.read_csv(name)
    #マージしてしまう
    df_merged=pd.merge(df_tanna,df_amedas[name],left_on='amedas_time',right_on='mod_date')

# print(df_amedas[amedas_file_list[0]])
print(df_merged)

df_merged.to_csv(strOutputFile + '/integrated.csv')



#アメダスデータをループして結合してゆく
#こんなかんじ
# df3.to_csv('integrated.csv')
# >>> df2=pd.read_csv('50281_ajiro_ame_cleaned.csv')
# >>> df3=pd.merge(df,df2,left_on='amedas_time',right_on='mod_date')
# >>> df3.to_csv('integrated.csv')