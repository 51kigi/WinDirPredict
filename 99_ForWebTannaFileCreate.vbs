'丹那ファイルを順番に読み込んで時間、風向のタブ区切りのファイルを作成
'https://mirai.userlocal.jp/

str_outfile="C:\Users\k\Documents\test\data\99_OutFileForWeb.tsv"
dim fso
set fso=createobject("Scripting.FileSystemObject")
set objOutFile=fso.OpenTextFile(str_outfile,2,True)
dim folder
set folder=fso.getFolder("C:\Users\k\Documents\test\data")

dim file
for each file in folder.Files
    if left(file.name,19)="tannna_original_v2_" then
        wscript.echo file.name
        set objfile=fso.OpenTextFile(folder.name & "\" & file.name)
        do while objfile.atEndOfStream<>True
            tmp_str_line= objFile.ReadLine
            tmp_str_array_line=split(tmp_str_line,",")
            tmp_date_time=DateAdd("h",9,DateAdd("s",tmp_str_array_line(0),DateSerial(1970,1,1)))
            tmp_windDir=round(tmp_str_array_line(4)*360/255,2)
            'Wscript.echo "org:" & tmp_str_array_line(0) & vbtab & tmp_str_array_line(4)
            'Wscript.echo "map:" & tmp_date_time & vbtab & tmp_windDir
            objOutFile.writeline tmp_date_time & vbtab & tmp_windDir

        loop
    end if
next