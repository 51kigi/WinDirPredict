'ExcelでVlookすると非常に時間がかかるのでスクリプトで一気にやってしまうテスト
'http://bayashita.com/p/entry/show/83  (参考)
'http://www.kanaya440.com/contents/script/vbs/function/data/cdate.html
'http://www.symmetric.co.jp/blog/archives/17
'20170902時間の制限を入れないようにする(夜の時間帯もデータに入れるようにする）

Dim objFileSys
Dim strFilePath_mishima
Dim strFilePath_aziro
Dim strFileContents
Dim objReadStream_mishima
Dim objReadStream_aziro
Dim OutputFile

'対象のファイルのパスを指定
'strFilePath_mishima = "C:\Users\k\Documents\test\test_mishima.csv"
'strFilePath_aziro="C:\Users\k\Documents\test\test_aziro.csv"
strFilePath_mishima = "C:\Users\k\Documents\test\50206_sizuoka_mishima_20140701-20170425_amadas.csv"
strFilePath_aziro="C:\Users\k\Documents\test\50281_kanagawa_aziro_20140701-20170425_amedas.csv"
 
'ファイルシステムを扱うオブジェクトを作成
Set objFileSys = CreateObject("Scripting.FileSystemObject")
 
'ファイルを読み取り専用で開き、TextStream オブジェクトを取得
Set objReadStream_mishima = objFileSys.OpenTextFile(strFilePath_mishima, 1)
Set objReadStream_aziro = objFileSys.OpenTextFile(strFilePath_aziro, 1)
'Set OutputFile=objFileSys.OpenTextFile("C:\Users\k\Documents\test\integrated_test.csv",2,true)
Set OutputFile=objFileSys.OpenTextFile("C:\Users\k\Documents\test\integrated_amedas_v2_1.csv",2,true)

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
filtered_outstr="mishima_id,aziro_id,date,time,mishima_dir,mishima_speed,aziro_dir,aziro_speed" 
OutputFile.WriteLine filtered_outstr

for i=2 to ubound(array_mishima)
    tmp_mishima=split(array_mishima(i),",")
    tmp_aziro=split(array_aziro(i),",")
    'Wscript.Echo(tmp_mishima(0))
    if tmp_mishima(1)=tmp_aziro(1) then
        buf_time=split(tmp_mishima(1),"-")
        check_time=cdate(buf_time(1))
        '20160113以降しか丹那のデータはないので、アメダスデータもそれ以降にしておく（後続マッチング処理でマッチさせるように）
        'if TimeValue("8:00:00") <= check_time And check_time <= TimeValue("18:00:00") And DateValue(buf_time(0))>DateValue("2016/1/14") then
            outstr= tmp_mishima(0) & "," & tmp_aziro(0) & "," & buf_time(0) & "," & buf_time(1) & "," & tmp_mishima(3) & "," &_
                tmp_mishima(4) & "," & tmp_aziro(3) & "," & tmp_aziro(4) 
            'Wscript.Echo(outstr)   
            OutputFile.WriteLine outstr
        'end if
    else
        Wscript.Echo("unmatch:" & i)
        exit for
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