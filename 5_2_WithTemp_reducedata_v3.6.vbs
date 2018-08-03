'全体マージしたファイルの中から必要なデータだけを取り出して
'Rにかけるデータ量を少なくする
'4_v3.2対応

Dim objFileSys
Dim strFilePath_Reduce
Dim strFilePath_Reduced
Dim objReadStream_reduce
Dim strOutputFilePath

'対象のファイルを設定
strFilePath_Reduce=".\data\4_WithTemp_united_amedas_tanna_test3.5.csv"
strFilePath_Reduced=".\data\5_WithTemp_reduced_united_test3.5.csv"

'ファイルシステムオブジェクト設定
set objFileSys=CreateObject("Scripting.FilesystemObject")

'統合ファイルを読み込み,配列に
set objReadStream_reduce=objFileSys.OpenTextFile(strFilePath_Reduce)
array_integrated=split(objReadStream_reduce.ReadAll,vbcrlf)

'Outputファイルの設定
set objOutputFile=objFileSys.OpenTextFile(strFilePath_Reduced,2,true)

'データを絞るために網代、三島、丹那の風向風力と判定だけにする
'mishima_id,aziro_id,date,time,mishima_dir,mishima_speed,aziro_dir,aziro_speed,tanna_date,tanna_time,tannna_dir,tanna_speed,tanna_date+3,tanna_time+3,tannna_dir+3,tanna_speed+3,judge
'必要なのは4,5,6,7,10,11,16

'outstr="mishima_dir,mishima_spd,aziro_dir,aziro_spd,tan_dir,tan_spd,judge"
'objOutputFile.WriteLine outstr

for i=lbound(array_integrated) to ubound(array_integrated)
    'Wscript.echo array_integrated(i)
    line_array_integrated=split(array_integrated(i),",")
    if ubound(line_array_integrated)>11 then
        'outstr=line_array_integrated(4) & "," & _
        '    line_array_integrated(5) & "," & _
        '    line_array_integrated(6) & "," & _
        '    line_array_integrated(7) & "," & _
        '    line_array_integrated(10) & "," & _
        '    line_array_integrated(11) & "," & _
        '    line_array_integrated(12)

        outstr=line_array_integrated(4) & "," & _
            line_array_integrated(5) & "," & _
            line_array_integrated(6) & "," & _
            line_array_integrated(7) & "," & _
            line_array_integrated(8) & "," & _
            line_array_integrated(9) & "," & _
            line_array_integrated(12) & "," & _
            line_array_integrated(13) & "," & _
            line_array_integrated(18) 


        objOutputFile.WriteLine outstr
    end if
next