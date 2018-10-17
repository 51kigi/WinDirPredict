'丹那データをJSONで取り出しファイル出力する
'https://o10e.org/blog/how-to-parse-json-for-vbscript/
'http://www.majishini.net/wp/?p=451
'32bitのcmdで実行する　%SystemRoot%\SysWow64\cscript.exe
'ScriptControlが64bit対応していないため

'アプローチをV1と変える
'１、丹那データを順番に読み込み、各データの一番近い10分の時刻をつけて出力
'２、出力したデータの中で、同じ10分を持つものについてはより近いほうを正のデータとして再出力

Dim objReadStream_tanna
Dim ten_min
dim folder

'何かしら引数がセットされていたらテストモードをONにする
if Wscript.Arguments.Count>0 then
    testmode=1
else
    testmode=0
end if

set objFileSys=CreateObject("Scripting.FileSystemObject")
'取得ファイルを定義
strInputFilePath=".\data\raw\1_tanna\tannna_original_v2.csv"
'出力ファイル名を定義
strOutputFilePath=".\data\raw\1_tanna\00_tmp_tannna_cleaned.csv"
strOutputFilePath2=".\data\raw\1_tanna\01_tannna_cleaned.csv"
'取得データのヘッダー
strInHeader="unix,max,min,avg,dir,date"
'出力データのヘッダー
'amadas_timeは"2016/01/10-03:10:00"のようなフォーマットだが、今は普通のフォーマットで
strOutHeader="amdas_time,unix,max,min,avg,dir,date,filename"

'ファイルリストを取得
set FSO=CreateObject("Scripting.FileSystemObject")
set folder=fso.getFolder(".\data\raw\1_tanna")

'出力ファイルオープン
set OutputFile=objFileSys.OpenTextFile(strOutputFilePath,2,true)
'各ファイルに対してループを回す
wscript.echo("start first step " & Now)
for each file in folder.files
    if InStr(1,file.name,"tannna_original_v2_") then
        if testmode=1 then
            wscript.echo(file.name)
        end if
        '丹那データを読み込み配列に格納
        set objReadStream_tanna=objFileSys.OpenTextFile(".\data\raw\1_tanna\" & file.name)
        tmp_tanna_array=split(objReadStream_tanna.ReadAll,vbcrlf)
        objReadStream_tanna.close
        ' 全ての行について直近の10分をセットして出力
        for i=0 to ubound(tmp_tanna_array)
            tmp_tanna_line_array=split(tmp_tanna_array(i),",")
            if ubound(tmp_tanna_line_array)>0 then
                tmp_tanna_time=CDate(tmp_tanna_line_array(5))
                if testmode=1 then
                    wscript.echo("tmp_tanna_time:" & tmp_tanna_time)
                end if
                '直近の10分を決める
                ten_min=round(Minute(tmp_tanna_time)/10)*10
                if ten_min="60" then
                    if testmode=1 then
                        wscript.echo("60check")
                    end if
                    if Hour(tmp_tanna_time)+1=24 then
                        if testmode=1 then
                            wscript.echo("24check")
                        end if
                        '一日足してから時間分を修正する
                        tmp_tanna_time=DateAdd("d",1,tmp_tanna_time)
                        judge_time=Year(tmp_tanna_time) & "/" & Month(tmp_tanna_time) & "/" & Day(tmp_tanna_time) & " " &_
                        "0" & ":" & "00" & ":00"
                    else
                        judge_time=Year(tmp_tanna_time) & "/" & Month(tmp_tanna_time) & "/" & Day(tmp_tanna_time) & " " &_
                        Hour(tmp_tanna_time)+1 & ":" & "00" & ":00"
                    end if
                elseif ten_min="0" then
                    judge_time=Year(tmp_tanna_time) & "/" & Month(tmp_tanna_time) & "/" & Day(tmp_tanna_time) & " " &_
                    Hour(tmp_tanna_time) & ":" & "00" & ":00"
                else
                    judge_time=Year(tmp_tanna_time) & "/" & Month(tmp_tanna_time) & "/" & Day(tmp_tanna_time) & " " &_
                    Hour(tmp_tanna_time) & ":" & ten_min & ":00"
                end if

                outstr=FormatDateTime(judge_time,vbShortDate) & " " & FormatDateTime(judge_time,vbShortTime)
                for j=0 to ubound(tmp_tanna_line_array)
                    outstr=outstr & "," & tmp_tanna_line_array(j)
                next
                outstr=outstr & "," & file.name
                OutputFile.WriteLine outstr
                outstr=""
            end if
        next
    end if
next
OutputFile.close

Wscript.echo("start second step " & Now)

'たった今クローズしたファイルをオープン
set objReadStream_tanna2=objFileSys.OpenTextFile(strOutputFilePath)
tmp_tanna_array=split(objReadStream_tanna2.ReadAll,vbcrlf)
objReadStream_tanna2.close
'最終的に出力するファイルをオープン
set OutputFile=objFileSys.OpenTextFile(strOutputFilePath2,2,true)
'とりあえず1行目をセットしておく
'ループの中では直前と比較しながら出力候補を決めてゆく
OutputFile.WriteLine strOutHeader
prev_array=tmp_tanna_array(0)
for i=0 to ubound(tmp_tanna_array)
    prev_line_array=split(prev_array,",")
    tmp_tanna_line_array=split(tmp_tanna_array(i),",")
    if ubound(tmp_tanna_line_array)>0 then
        'amedas時間が変わったら出力候補をかきだす
        if prev_line_array(0)<>tmp_tanna_line_array(0) then
            outstr=prev_line_array(0)
            for j=1 to ubound(prev_line_array)
                outstr=outstr & "," & prev_line_array(j)
            next
            OutputFile.WriteLine outstr
            if testmode=1 then
                Wscript.echo("amedas time:" & prev_line_array(0) & "### tanna time:" & prev_line_array(6))
            end if
            outstr=""
            prev_array=tmp_tanna_array(i)
        'amedas時間が同じ場合、よりamedas時間に近いほうに出力候補を入れ替える
        elseif abs(DateDiff("n",prev_line_array(0),prev_line_array(6)))>abs(DateDiff("n",tmp_tanna_line_array(0),tmp_tanna_line_array(6))) then
            if testmode=1 then
                Wscript.echo("amedas time:" & tmp_tanna_line_array(0) & "### tanna time:" & tmp_tanna_line_array(6))
            end if
            prev_array=tmp_tanna_array(i)
        end if
    else
    '比較対象が後続にないので書き出してしまう
        outstr=prev_line_array(0)
        for j=1 to ubound(prev_line_array)
            outstr=outstr & "," & prev_line_array(j)
        next
        if testmode=1 then
            Wscript.echo("amedas time:" & prev_line_array(0) & "### tanna time:" & prev_line_array(6))
        end if
        outstr=""
    end if
next
OutputFile.close

Wscript.echo("end" & Now)