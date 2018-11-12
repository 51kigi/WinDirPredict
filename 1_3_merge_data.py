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

df_merged=df_tanna
#リストのインデックスは整数でなければならないので辞書型の中にリストを入れ込む
df_amedas={}
for name in amedas_file_list:
    print(name)
    df_amedas[name]=pd.read_csv(name)
    #マージしてしまう
    df_merged=pd.merge(df_merged,df_amedas[name],left_on='amedas_time',right_on='mod_date')

    #amedasを次々マージしてゆくのでヘッダーを調整しておく
    #まず今のヘッダーをリストで取得
    col_list=df_merged.columns.values
    rename_col={}
    amedas_name=name.split("_")
    #先頭の丹那部分は不変、以降のamedas部分にファイル名から切り出したamedas拠点の名前を入れる
    #(最後の7つが変更の対象)
    for i in range(len(col_list)):
        if i<len(col_list)-7:
            rename_col[col_list[i]]=col_list[i]
        else:
            #名前を取り出すインデックス番号の決め方は微妙、、
            rename_col[col_list[i]]=col_list[i]+"_"+amedas_name[2]
    #辞書型に入れた変更後ヘッダーをセット
    df_merged=df_merged.rename(columns=rename_col)

#indexは不要
df_merged.to_csv(strOutputFile + '/integrated.csv',index=False)



#アメダスデータをループして結合してゆく
#こんなかんじ
# df3.to_csv('integrated.csv')
# >>> df2=pd.read_csv('50281_ajiro_ame_cleaned.csv')
# >>> df3=pd.merge(df,df2,left_on='amedas_time',right_on='mod_date')
# >>> df3.to_csv('integrated.csv')