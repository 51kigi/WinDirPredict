'マージしたAMEDASファイルに随時読み出した丹那データをマッチさせてゆく
'随時読み出しの場合、アメダス側のデータにヒットする丹那データがない場合に次のアメダスデータに戻れないので、
'丹那データもメモリ上げするバージョン
'mishima,aziro,tanna,tanna+3でデータを作るバージョン
'読み込むアメダスデータは夜間も対象にしたほう
'結果の判定をOK/NGから1，2，3，4に変更
'結果の判定を方位風速に応じて行うように変更
'風速3.5m以上は10の位を２、それ以下は１
'方位は一の位　北から北東を0
'             北東から東を２
'　　　　　　　東から南東を２
'             南東から南を４
'　　　　　　　南から南西を4
'　　　　　　　南西から西を６
'　　　　　　　西から北西を６
'　　　　　　　北西から北を0

Dim objFileSys
Dim strFilePath_integrated
Dim strFilePath_tanna
Dim objReadStream_integrated
Dim objReadStream_tanna1
Dim objReadStream_tanna2
Dim objReadStream_tanna3
Dim strFilePath_tmp_tanna
Dim strOutputFilePath

'対象ファイルのパスを設定
strFilePath_integrated= ".\data\3_integrated_amedas_v2_1.csv"
strFilePath_tanna=".\data\raw\1_tanna\tannna_original_v2_"
strFilePath_tmp_tanna=".\data\tmp_tanna.csv"
strOutputFilePath=".\data\4_united_amedas_tanna_test3.5.csv"


'ファイルシステムオブジェクト作成
set objFileSys=CreateObject("Scripting.FileSystemObject")

'AMAEDASファイルを読み込んで配列としてメモリあげ
Set objReadStream_integrated=objFileSys.OpenTextFile(strFilePath_integrated,1)
'丹那ファイルの設定  

'Outputファイルの設定
Set objOutputFile=objFileSys.OpenTextFile(strOutputFilePath,2,true)


array_amedas=split(objReadStream_integrated.ReadAll,vbcrlf)
'array_tanna=split(objReadStream_tanna.ReadAll,vblf)
'Header文字格納
outstr="mishima_id,aziro_id,date,time,mishima_dir,mishima_speed,aziro_dir,aziro_speed,tanna_date,tanna_time,tannna_dir,tanna_speed,tanna_date+3,tanna_time+3,tannna_dir+3,tanna_speed+3,judge"
objOutputFile.WriteLine outstr
outstr=""

'amedasファイルを一行ずつ回す

'Wscript.echo ubound(array_amedas)

tanna_line_cnt=1

'前回ループ時のアメダスの日付
prev_amedas_date=""

'ループはアメダスを基本に回す
for i=lbound(array_amedas)+1 to ubound(array_amedas)-1
    line_array_amedas=split(array_amedas(i),",")
    '前回処理時とアメダス日付が変わらない場合は丹那ファイル読み出しをしない
    '前回処理時とアメダス日付が変わる場合は丹那ファイルの読出しから行う
    if prev_amedas_date=line_array_amedas(2)  then
    else
        if objFileSys.FileExists(strFilePath_tmp_tanna) then
            ret=objFileSys.DeleteFile(strFilePath_tmp_tanna,True)
        end if
        Wscript.echo(strFilePath_tmp_tanna)
        Set objtmptanna=objFileSys.OpenTextFile(strFilePath_tmp_tanna,8,True)
        '前回処理日付を更新
        'Wscript.echo line_array_amedas(2)
        prev_amedas_date=line_array_amedas(2)
        '読出し用丹那ファイル名合成用の文字列を作成
        tanna_date1=Year(prev_amedas_date) & Right("0" & Month(prev_amedas_date),2) & Right("0" & (day(prev_amedas_date)-1),2)
        tanna_date2=Year(prev_amedas_date) & Right("0" & Month(prev_amedas_date),2) & Right("0" & day(prev_amedas_date),2)
        tanna_date3=Year(prev_amedas_date) & Right("0" & Month(prev_amedas_date),2) & Right("0" & (day(prev_amedas_date)+1),2)
        'まとめようファイルの初期化
        objtmptanna.Write ""

        '丹那ファイルはアメダスデータの日付により可変で読み込み
       'ファイルを連結して一つのファイルにし、そのファイルを読み込んで一気に配列に入れる
        'ReadAllを三ファイル分回す
        '空ファイルがあるとReadAllでこけるので、ファイルの状態を事前に整えておく
 
        Wscript.echo strFilePath_tanna & tanna_date1 & ".csv"
        wscript.echo("1:" & strFilePath_tanna & tanna_date1 & ".csv")
        wscript.echo("2:" & strFilePath_tanna & tanna_date2 & ".csv")
        wscript.echo("3:" & strFilePath_tanna & tanna_date3 & ".csv")


        if objFileSys.FileExists(strFilePath_tanna & tanna_date1 & ".csv") then
            Set objReadStream_tanna1=objFileSys.OpenTextFile(strFilePath_tanna & tanna_date1 & ".csv",1)
            tmp_tanna=objReadStream_tanna1.ReadAll
            objReadStream_tanna1.close
            objtmptanna.Write tmp_tanna
        end if
        
        if objFileSys.FileExists(strFilePath_tanna & tanna_date2 & ".csv") then
            Set objReadStream_tanna2=objFileSys.OpenTextFile(strFilePath_tanna & tanna_date2 & ".csv",1)
            tmp_tanna=objReadStream_tanna2.ReadAll
            objReadStream_tanna2.close
            objtmptanna.Write tmp_tanna
        end if

        if objFileSys.FileExists(strFilePath_tanna & tanna_date3 & ".csv") then
            Set objReadStream_tanna3=objFileSys.OpenTextFile(strFilePath_tanna & tanna_date3 & ".csv",1) 
            tmp_tanna=objReadStream_tanna3.ReadAll
            objReadStream_tanna3.close
            objtmptanna.Write tmp_tanna
        end if

        'Set objtmptanna=objFileSys.OpenTextFile(strFilePath_tmp_tanna,2,true)
        objtmptanna.close
        set objReadStream_tmp_tanna=objFileSys.OpenTextFile(strFilePath_tmp_tanna,1)
        'ファイルが空だとReadAllでエラーが出る
        if objReadStream_tmp_tanna.AtEndOfStream then
            'Wscript.echo "tmp_tanna is null "
            objReadStream_tmp_tanna.close
        else
            tmp_objtmptanna=objReadStream_tmp_tanna.ReadAll
            objReadStream_tmp_tanna.close
        end if
    end if
    
    '同時刻の丹那を連結
if tmp_objtmptanna<>"" then
        array_tanna=split(tmp_objtmptanna,vblf)
        '丹那の配列を回し、マッチするデータを探す　ない場合はなしで次のアメダスデータに行く（出力なし）
        for j=lbound(array_tanna) to ubound(array_tanna)
                buf_tanna=trim(array_tanna(j))
                ' '空行でないときだけ処理をする
                    if buf_tanna<>"" then
                    line_array_tanna=split(buf_tanna,",")
                '     'Unix時間を普通の時間に変更　UTCからJSTに直す
                    tmp_time_tanna=DateAdd("h",9,DateAdd("s",line_array_tanna(0),DateSerial(1970,1,1)))
                    if DateDiff("d",CDate(line_array_amedas(2)),DateValue(CDate(tmp_time_tanna)))=0 then
                        '時間でマッチ　完全一致ではなく10分以内で
                        if Abs(DateDiff("n",CDate(line_array_amedas(3)),TimeValue(CDate(tmp_time_tanna))))<10 then
                            '丹那が西風であればOKをセット、それ以外はNGをセット
                            outstr=replace(array_amedas(i),vbcr,"") & "," &_
                                    DateValue(CDate(tmp_time_tanna)) & "," & TimeValue(CDate(tmp_time_tanna)) & "," & line_array_tanna(4) &_
                                    "," & line_array_tanna(3)
                            exit for
                            tanna_line_cnt=j
                        end if   
                    end if
                end if
            next
    end if


    '3時間後の丹那を連結し、判定する
    '丹那の方額は255で360を現していることに注意
    if tmp_objtmptanna<>"" then
        array_tanna=split(tmp_objtmptanna,vblf)
        '丹那の配列を回し、マッチするデータを探す　ない場合はなしで次のアメダスデータに行く（出力なし）
        for j=lbound(array_tanna) to ubound(array_tanna)
                buf_tanna=trim(array_tanna(j))
                ' '空行でないときだけ処理をする
                    if buf_tanna<>"" then
                        line_array_tanna=split(buf_tanna,",")
                    '     'Unix時間を普通の時間に変更　UTCからJSTに直す
                        tmp_time_tanna=DateAdd("h",9,DateAdd("s",line_array_tanna(0),DateSerial(1970,1,1)))
                        if DateDiff("d",CDate(line_array_amedas(2)),DateValue(CDate(tmp_time_tanna)))=0 then
                            '時間でマッチ　完全一致ではなく3分以内で 丹那側は3時間進める
                            if Abs(DateDiff("n",CDate(line_array_amedas(3)),TimeValue(DateAdd("h",-3,CDate(tmp_time_tanna)))))<10 then
                                '北から北東を０
                                '北東から東を２
                                '東から南東を２
                                '南東から南を４
                                '南から南西を４
                                '南西から西を６
                                '西から北西を６
                                '北西から北を０
                                if line_array_tanna(4)>=0.0 and line_array_tanna(4)<=31.88 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="20"
                                    else
                                        dir_judge="10"
                                    end if
                                elseif line_array_tanna(4)>31.88 and line_array_tanna(4)<=63.76 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="22"
                                    else
                                        dir_judge="12"
                                    end if
                                elseif line_array_tanna(4)>63.76 and line_array_tanna(4)<=95.64 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="22"
                                    else
                                        dir_judge="12"
                                    end if
                                elseif line_array_tanna(4)>95.64 and line_array_tanna(4)<=127.52 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="24"
                                    else
                                        dir_judge="14"
                                    end if
                                elseif line_array_tanna(4)>127.52 and line_array_tanna(4)<=159.4 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="24"
                                    else
                                        dir_judge="14"
                                    end if
                                elseif line_array_tanna(4)>159.4 and line_array_tanna(4)<=191.28 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="26"
                                    else
                                        dir_judge="16"
                                    end if
                                elseif line_array_tanna(4)>191.28 and line_array_tanna(4)<=223.16 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="26"
                                    else
                                        dir_judge="16"
                                    end if
                                elseif line_array_tanna(4)>223.16 and line_array_tanna(4)<=256.0 then
                                    if line_array_tanna(3)>35 then
                                        dir_judge="20"
                                    else
                                        dir_judge="10"
                                    end if
                                else
                                    dir_judge="99"
                                end if
                                if outstr<>"" then
                                    outstr=outstr & "," &_
                                            DateValue(CDate(tmp_time_tanna)) & "," & TimeValue(CDate(tmp_time_tanna)) & "," & line_array_tanna(4) &_
                                            "," & line_array_tanna(3) & "," & dir_judge
                                    objOutputFile.WriteLine outstr
                                    outstr=""
                                end if
                                exit for
                                tanna_line_cnt=j
                            end if   
                    end if
                end if
            next
    else
    end if
next

'objOutputFile.write outstr

objOutputFile.close
objReadStream_integrated.close
set objFileSys=Nothing

Wscript.echo ("end")
