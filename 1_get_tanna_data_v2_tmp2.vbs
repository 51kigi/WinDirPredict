'丹那データをJSONで取り出しファイル出力する
'https://o10e.org/blog/how-to-parse-json-for-vbscript/
'http://www.majishini.net/wp/?p=451
'32bitのcmdで実行する　%SystemRoot%\SysWow64\cscript.exe
'ScriptControlが64bit対応していないため

Function parseJson (ByVal strJson)  
  Dim objJs

  Set objJs = CreateObject("ScriptControl")
  objJs.Language = "JScript"
  objJs.AddCode "function jsonParse(str) { return eval('(' + str + ')'); };"

  Set parseJson = objJs.CodeObject.jsonParse(strJson)
End Function

Dim strJson  
Dim objJs  
Dim objJson
Dim objFileSys
Dim strOutputFilePath
Dim OutputFile
Dim OutputFile2

'commandラインから日付の引数を取得
if Wscript.Arguments.Count=0 then
else
    tmpDate=Wscript.Arguments(0)
end if

Wscript.echo tmpDate

Wscript.echo "start"

'strOutputFilePath="C:\Users\k\Documents\test\tannna_original_v2.csv"
set oShell=CreateObject("Wscript.Shell")

'script実行ディレクトリからの相対ディレクトリで動くように変更(20180721)
'strHomeFolder=oShell.ExpandEnvironmentStrings("%HOMEPATH%")
'

'strOutputFilePath=strHomeFolder & "\Documents\test\data\tannna_original_v2.csv"
'strOutputFilePath2=strHomeFolder & "\Documents\test\data\tannna_original_v2_"

strOutputFilePath=".\data\raw\1_tanna\tannna_original_v2.csv"
strOutputFilePath2=".\data\raw\1_tanna\tannna_original_v2_"

set objFileSys=CreateObject("Scripting.FileSystemObject")

Wscript.echo strOutputFilePath

set OutputFile=objFileSys.OpenTextFile(strOutputFilePath,2,true)


'　ScriptControlのオブジェクトを作成  
'Set objJs = CreateObject("ScriptControl")  
' 言語にJScriptを指定  
'objJs.Language = "JScript"  
' Jsonをパースする関数の追加  
'objJs.AddCode "function jsonParse(str) { return eval('(' + str + ')'); };"
if tmpDate<>"" then
    startDate=tmpDate
else
    startDate = "2017/10/30"
end if
monthstrlen=2
daystrlen=2
stuffStr=0

'指定の日付から今日までの日数をカウント
datediffcnt=DateDiff("d",startDate,Now)
Wscript.echo("datediff:" & datediffcnt)
Wscript.sleep(2000)
'JSONデータをPOSTで取得して都度Parseし、ファイルに出力
for i=1 to 210
    '日付を一日進める
    startDate=DateAdd("d",1,startDate)
    Wscript.echo "processing:" & startDate & " process start at:" & Now()
    startYear=year(startDate)
    startMonth=replace(space(monthstrlen-len(month(startDate) )) & month(startDate),space(1),stuffStr)  
    Startday=replace(space(daystrlen-len(day(startDate)))&day(startDate) ,space(1),stuffStr)

    Wscript.echo startYear & startMonth & Startday
    
    TARGET_URL = "http://rdc.dip.jp/getDB.php?mode=json&id=1&date=" & startYear & startMonth & Startday
    sendData = ""
    
    Wscript.echo TARGET_URL

    Set httpObj = CreateObject("MSXML2.XMLHTTP")
    httpObj.Open "GET", TARGET_URL, False
    httpObj.send (sendData)

    strJSON = httpObj.ResponseText
    '#recordをrecordidに置換
    strJSON = Replace(strJSON, """recode"":", """recid"":")
    strJSON = Replace(strJSON, """max"":", """maxnum"":")
    strJSON = Replace(strJSON, """min"":", """minnum"":")
    strJSON = Replace(strJSON, """avg"":", """avgnum"":")
    
    ' 引数にJSON形式の文字列を渡して実行  
    'Set objJson = objJs.CodeObject.jsonParse(strJson)
    Set objJson = parseJson(strJson)

    set OutputFile2=objFileSys.OpenTextFile(strOutputFilePath2 & startYear & startMonth & Startday & ".csv",2,true)

    For Each rec IN objJson.recid
        outStr=rec.unix & "," & rec.maxnum & "," & rec.minnum & "," & rec.avgnum & "," & rec.direc & "," &_
               DateAdd("h",9,DateAdd("s",rec.unix,DateSerial(1970,1,1))) 
        OutputFile.WriteLine outStr
        OutputFile2.WriteLine outStr
    next
    Wscript.echo("start sleep:" & Now())
    OutputFile2.close
    Wscript.sleep 30000
next
OutputFile.close

Wscript.echo "end"