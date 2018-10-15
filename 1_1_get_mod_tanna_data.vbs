'丹那データをJSONで取り出しファイル出力する
'https://o10e.org/blog/how-to-parse-json-for-vbscript/
'http://www.majishini.net/wp/?p=451
'32bitのcmdで実行する　%SystemRoot%\SysWow64\cscript.exe
'ScriptControlが64bit対応していないため

'1_get_tanna_data_v2_tmpで取得したファイルがフォルダにある前提
'10分毎のデータ(アメダスのデータが10分置きなので）に整形する
'0,ファイルリストを取得して、各ファイルに対してループを回す
'1,ファイルにある最初のデータの日付、時間を取得し、直近の10分の時間のデータとする
'2,次のデータからは直近の前後の10分の近いほうの候補とし、前回のデータとより近いほうを姓のデータとして採用する
'3,決定したデータからファイルに出力してゆく
'4,最後に出力したファイルの中にある重複データ(重複している10分のデータ）があるか確認し、存在する場合はより近いほうを採用する

Dim objReadStream_tanna
Dim ten_min
dim folder

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

'ファイルリストを取得
set FSO=CreateObject("Scripting.FileSystemObject")
set folder=fso.getFolder(".\data\raw\1_tanna")

'出力ファイルオープン
set OutputFile=objFileSys.OpenTextFile(strOutputFilePath,2,true)
'各ファイルに対してループを回す
for each file in folder.files
    if InStr(1,file.name,"tannna_original_v2_") then
        'wscript.echo(file.name)

        '丹那データを読み込み配列に格納
        set objReadStream_tanna=objFileSys.OpenTextFile(".\data\raw\1_tanna\" & file.name)
        tmp_tanna_array=split(objReadStream_tanna.ReadAll,vbcrlf)
        objReadStream_tanna.close
        '一行目のデータから日付を取得し、最初の10分時刻を確定
        tanna_date_line_array=split(tmp_tanna_array(0),",")
        tmp_first_time=CDate(tanna_date_line_array(5))

        '## 時間処理確認用テストコード
        ' temp_tmp_first_time="2018/08/28 19:56:26"
        ' tmp_first_time=CDate(temp_tmp_first_time)
        '##
        '-- 分を取得し、10分の一をして四捨五入、そのうえで10倍する(どちらかの10分による）
        '-- 60になったら0にする
        'wscript.echo("tmp_first_time:" & tmp_first_time)
        ten_min=round(Minute(tmp_first_time)/10)*10
        if ten_min="60" then
            wscript.echo("60check")
            if Hour(tmp_first_time)+1=24 then
                wscript.echo("24check")
                '一日足してから時間分を修正する
                tmp_first_time=DateAdd("d",1,tmp_first_time)
                judge_time=Year(tmp_first_time) & "/" & Month(tmp_first_time) & "/" & Day(tmp_first_time) & " " &_
                "0" & ":" & "00" & ":00"
            else
                judge_time=Year(tmp_first_time) & "/" & Month(tmp_first_time) & "/" & Day(tmp_first_time) & " " &_
                Hour(tmp_first_time)+1 & ":" & "00" & ":00"
            end if
        elseif ten_min="0" then
            judge_time=Year(tmp_first_time) & "/" & Month(tmp_first_time) & "/" & Day(tmp_first_time) & " " &_
            Hour(tmp_first_time) & ":" & "00" & ":00"
        end if

        ' judge_time=Year(tmp_first_time) & "/" & Month(tmp_first_time) & "/" & Day(tmp_first_time) & " " &_
        ' Hour(tmp_first_time) & ":" & ten_min & ":00" ' & Second(tmp_first_time)

        'ループの最初でしようする前回までの一番近い時間のデータの配列
        prev_time_value=tanna_date_line_array
        wscript.echo("prev value:" & prev_time_value(5))
        'ループですべての行に対して処理を行う
        for i=0 to ubound(tmp_tanna_array)
            each_tanna_line_array=split(tmp_tanna_array(i),",")
            if ubound(each_tanna_line_array)>1 then
                test_date_time=each_tanna_line_array(5)
                Wscript.echo("judge value:" & judge_time & "###" & "current value:" & test_date_time)

                if DateDiff("n",judge_time,test_date_time)>5 then
                    'wscript.echo("found data for " & judge_time & "###" & prev_time_value(5))
                    'judge_timeだけで出力すると00:00が省略されてしまうのでわざわざフォーマットして出力
                    outstr=FormatDateTime(judge_time,vbShortDate) & " " & FormatDateTime(judge_time,vbShortTime)
                    for j=0 to ubound(prev_time_value)
                        outstr=outstr & "," & prev_time_value(j)
                    next
                    outstr=outstr & "," & file.name
                    OutputFile.WriteLine outstr
                    prev_time_value=each_tanna_line_array
                    judge_time=DateAdd("n",10,judge_time)
                    wscript.echo("change judgetime:" & FormatDateTime(judge_time,vbShortTime))
                '前回の時刻とJudgeTimeの分の差よりも今回の時刻とJudgeTime分の差のほうが近ければ前回の時刻を更新
                elseif abs(DateDiff("s",each_tanna_line_array(5),judge_time))<abs(DateDiff("s",prev_time_value(5),judge_time)) then
                    'wscript.echo("change:" & each_tanna_line_array(5))
                    prev_time_value=each_tanna_line_array
                end if
                'wscript.echo(test_date_time)
            else

            end if

        next
        wscript.echo("end")

        ' Wscript.echo(ten_min)
        ' Wscript.echo(tmp_first_time)
        ' Wscript.echo(judge_time)

        ' tmp_test_date="2016/01/10-03:10:00"
        ' Wscript.echo(IsDate(tmp_test_date))  'true(-1),false(0)
        ' Wscript.echo(IsDate(tmp_first_time))
        ' Wscript.echo(CDate(tmp_test_date))
    end if
next
OutputFile.close




