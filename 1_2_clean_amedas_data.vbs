'丹那データをJSONで取り出しファイル出力する
'https://o10e.org/blog/how-to-parse-json-for-vbscript/
'http://www.majishini.net/wp/?p=451
'32bitのcmdで実行する　%SystemRoot%\SysWow64\cscript.exe
'ScriptControlが64bit対応していないため

'アプローチをV1と変える
'１、amedasデータのファイルリストを取得
'２、ファイルを開き、各行のdataにある値を普通の日付型にした行を追加して新規ファイルに出力

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
strInputFilePath=".\data\raw\2_amedas\"
'出力ファイル名を定義
strOutputFilePath=".\data\raw\2_amedas\"

'ファイルリストを取得
set FSO=CreateObject("Scripting.FileSystemObject")
set folder=fso.getFolder(".\data\raw\2_amedas")

'各ファイルに対してループを回す
wscript.echo("start first step " & Now)
for each file in folder.files
    if InStr(1,file.name,"amedas_tsuuho.10min") then
        wscript.echo(file.name)
        'amedasデータを読み込み配列に格納
        set objReadStream_amedas=objFileSys.OpenTextFile(strInputFilePath & file.name)
        set OutputFile=objFileSys.OpenTextFile(strOutputFilePath & left(file.name,15) & "_cleaned.csv",2,true)
        tmp_amedas_array=split(objReadStream_amedas.ReadAll,vblf)
        objReadStream_amedas.close
        ' 全ての行についてdateカラムの値を普通の日付型に直してカラムを追加して出力
        ' wscript.echo(ubound(tmp_amedas_array))
        for i=1 to ubound(tmp_amedas_array)
            ' wscript.echo(i)
            tmp_amedas_line_array=split(tmp_amedas_array(i),",")
            if testmode=1 then
                wscript.echo(i & ":" & tmp_amedas_line_array(0))
            end if
            if i=1 then
                if testmode=1 then
                    wscript.echo("header:" & i)
                end if
                '1行目と2行目はヘッダーなのでそのまま出力
                for j=0 to ubound(tmp_amedas_line_array)
                    outstr=outstr & tmp_amedas_line_array(j)  & ","
                    wscript.echo("header " & i & ":" & tmp_amedas_line_array(j))
                next
                outstr=outstr & "mod_date"
                OutputFile.WriteLine outstr
                outstr=""
            else
                '3行目以降が実データなので処理を行う
                'といっても最後に付加する整形した日付だけがヘッダーと違う
                if testmode=1 then
                    wscript.echo("data line:" & i)
                end if
                if ubound(tmp_amedas_line_array)> 0 then
                    for j=0 to ubound(tmp_amedas_line_array)
                        outstr=outstr  & tmp_amedas_line_array(j) & ","
                    next
                    mod_date_str=split(tmp_amedas_line_array(1),"-")
                    tmp_amedas_time=mod_date_str(0) & " " & mod_date_str(1)
                    outstr=outstr  & FormatDateTime(tmp_amedas_time,vbShortDate) & " " & FormatDateTime(tmp_amedas_time,vbLongTime)
                    if testmode=1 then
                        wscript.echo("outstr:" & outstr)
                    end if
                    OutputFile.WriteLine outstr
                    outstr=""
                end if
            end if
        next
        OutputFile.close
    end if
next

Wscript.echo("end " & Now)