'ExcelでVlookすると非常に時間がかかるのでスクリプトで一気にやってしまうテスト
'http://bayashita.com/p/entry/show/83  (参考)
'http://www.kanaya440.com/contents/script/vbs/function/data/cdate.html
'http://www.symmetric.co.jp/blog/archives/17
'20170902時間の制限を入れないようにする(夜の時間帯もデータに入れるようにする）

'ファイル名に日本語入れないこと！
'最後はエラーで終わるがファイルはできているので気にしない!

Dim objFileSys
Dim strFilePath_mishima
Dim strFilePath_aziro
Dim strOutputFilepath
Dim strFileContents
Dim objReadStream_mishima
Dim objReadStream_aziro
Dim OutputFile

'対象のファイルのパスを指定
'スクリプト実行位置からの相対ディレクトリで
'ファイル名は都度手動、、
strFilePath_mishima = ".\data\raw\2_amedas\73151_mishima_amedas_tsuuho.10min180721010039.csv"
strFilePath_aziro=".\data\raw\2_amedas\50281_ajiro_amedas_tsuuho.10min180721010311.csv"
strOutputFilepath=".\data\3_WithTemp_integrated_amedas_v2_1.csv"

'カレントディレクトリ取得
dim objWshShell
Set objWshShell=Wscript.CreateObject("Wscript.shell")
strCurrentDirectory=objWshShell.CurrentDirectory

'ファイルシステムを扱うオブジェクトを作成
Set objFileSys = CreateObject("Scripting.FileSystemObject")
 
'ファイルを読み取り専用で開き、TextStream オブジェクトを取得
Set objReadStream_mishima = objFileSys.OpenTextFile(strFilePath_mishima, 1)
Set objReadStream_aziro = objFileSys.OpenTextFile(strFilePath_aziro, 1)
'Set OutputFile=objFileSys.OpenTextFile("C:\Users\k\Documents\test\integrated_test.csv",2,true)
Set OutputFile=objFileSys.OpenTextFile(strOutputFilepath,2,true)

'ファイル自体を行ごとに配列に格納
buf=objReadStream_mishima.ReadAll
array_mishima=split(buf,vblf)
buf=objReadStream_aziro.ReadAll
array_aziro=split(buf,vblf)

'配列の先頭文字でマッチし、マッチしたもの通しの内容をSplitして書き出し文字列を生成

tst=split(array_mishima(0),",")
for i=lbound(tst) to ubound(tst)
    'Wscript.Echo(tst(i))
next


Wscript.Echo("mishima array cnt:" & ubound(array_mishima) )
Wscript.Echo("aziro array cnt:" & ubound(array_aziro) )

'時間が一致していることはわかっているので配列の要素を合わせてどんどん結合してします
'メモリ展開したままだと処理が重くなってゆくので都度書き出ししてしまう
'先頭2行をスキップ(タイトル行なので）
filtered_outstr="mishima_id,aziro_id,date,time,mishima_dir,mishima_speed,mishima_tmp,aziro_dir,aziro_speed,ajiro_tmp" 
OutputFile.WriteLine filtered_outstr

for i=2 to ubound(array_mishima)
    tmp_mishima=split(array_mishima(i),",")
    tmp_aziro=split(array_aziro(i),",")
    '風向に511がセットされているものはデータとしてよろしくなさそうなので除外
    if tmp_mishima(3)<>"511" and tmp_aziro(3)<>"511" then
    
            'Wscript.Echo(tmp_mishima(0))
        if tmp_mishima(1)=tmp_aziro(1) then
            buf_time=split(tmp_mishima(1),"-")
            check_time=cdate(buf_time(1))
            '20160113以降しか丹那のデータはないので、アメダスデータもそれ以降にしておく（後続マッチング処理でマッチさせるように）
            'if TimeValue("8:00:00") <= check_time And check_time <= TimeValue("18:00:00") And DateValue(buf_time(0))>DateValue("2016/1/14") then
                outstr= tmp_mishima(0) & "," & tmp_aziro(0) & "," & buf_time(0) & "," & buf_time(1) & "," & tmp_mishima(3) & "," &_
                    tmp_mishima(4) & ","  & tmp_mishima(5) & "," & tmp_aziro(3) & "," & tmp_aziro(4) & "," &  tmp_aziro(5)
                'Wscript.Echo(outstr)   
                OutputFile.WriteLine outstr
            'end if
        else
            Wscript.Echo("unmatch:" & i)
            exit for
        end if
    end if

    if i mod 10000 =0 then
    Wscript.Echo(i)
    end if

next

OutputFile.close
objReadStream_mishima.Close
objReadStream_aziro.Close
Set objFileSys = Nothing 

Wscript.Echo("end")