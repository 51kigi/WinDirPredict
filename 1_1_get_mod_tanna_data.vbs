'丹那データをJSONで取り出しファイル出力する
'https://o10e.org/blog/how-to-parse-json-for-vbscript/
'http://www.majishini.net/wp/?p=451
'32bitのcmdで実行する　%SystemRoot%\SysWow64\cscript.exe
'ScriptControlが64bit対応していないため

'1_get_tanna_data_v2_tmpで取得したファイルがフォルダにある前提
'10分毎のデータ(アメダスのデータが10分置きなので）に整形する
'1,ファイルにある最初のデータの日付、時間を取得し、直近の10分の時間のデータとする
'2,次のデータからは直近の前後の10分の近いほうの候補とし、前回のデータとより近いほうを姓のデータとして採用する
'3,決定したデータからファイルに出力してゆく
'4,最後に出力したファイルの中にある重複データ(重複している10分のデータ）があるか確認し、存在する場合はより近いほうを採用する

Dim objReadStream_tanna
Dim ten_min

set objFileSys=CreateObject("Scripting.FileSystemObject")
'取得ファイルを定義
strInputFilePath=".\data\raw\1_tanna\tannna_original_v2.csv"
'出力ファイル名を定義
strOutputFilePath=".\data\raw\1_tanna\tannna_cleaned.csv"
'取得データのヘッダー
strInHeader="unix,max,min,avg,dir,date"
'出力データのヘッダー
'amadas_timeは"2016/01/10-03:10:00"のようなフォーマット
strOutHeader="amdas_time,unix,max,min,avg,dir,date"
'丹那データを読み込み配列に格納
set objReadStream_tanna=objFileSys.OpenTextFile(strInputFilePath)
tmp_tanna_array=split(objReadStream_tanna.ReadAll,vbcrlf)
objReadStream_tanna.close
'一行目のデータから日付を取得し、最初の10分時刻を確定
tanna_date_array=split(tmp_tanna_array(0),",")
tmp_first_time=CDate(tanna_date_array(5))

'## 時間処理確認用テストコード
' temp_tmp_first_time="2018/08/28 19:56:26"
' tmp_first_time=CDate(temp_tmp_first_time)
'##

'-- 分を取得し、10分の一をして四捨五入、そのうえで10倍する(どちらかの10分による）
'-- 60になったら0にする
ten_min=round(Minute(tmp_first_time)/10)*10
if ten_min="60" or ten_min="0" then
    ten_min="00"
end if

judge_time=Year(tmp_first_time) & "/" & Month(tmp_first_time) & "/" & Day(tmp_first_time) & " " &_
Hour(tmp_first_time) & ":" & ten_min & ":" & Second(tmp_first_time)

'ループですべての行に対して処理を行う
for i=0 to len(tmp_tanna_array)
    each_tanna_array=split(tmp_tanna_array(i),",")
    
next

Wscript.echo(ten_min)
Wscript.echo(tmp_first_time)
Wscript.echo(judge_time)

' tmp_test_date="2016/01/10-03:10:00"
' Wscript.echo(IsDate(tmp_test_date))  'true(-1),false(0)
' Wscript.echo(IsDate(tmp_first_time))
' Wscript.echo(CDate(tmp_test_date))



