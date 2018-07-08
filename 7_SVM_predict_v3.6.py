#v3.2対応
#読出しはすべてMydocument配下のファイルに変更
#options(encoding = "utf-8")を実行してRがSJISスクリプトを読めるようにする

#rからpythonへの移行

library("kernlab")
#MouseCompter用(ディレクトリは後で確認して姓の状態にする必要あり　2018/1/3)
model_Path_mouse="C:/Users/gk/Documents/test/6_weatherpredictmodel3.6"
data_Path_mouse="C:/Users/gk/Documents/test/7_input_for_predict_tanna.csv"
out_Path_mouse="C:/Users/gk/Documents/test/7_SVM_result.csv"
#Surface用
model_Path_Surface="C:/Users/k/Documents/test/6_weatherpredictmodel3.6"
data_Path_Surface="C:/Users/k/Documents/test/7_input_for_predict_tanna.csv"
out_Path_Surface="C:/Users/k/Documents/test/7_SVM_result.csv"

pc_select='mouse'

if (pc_select=='Surface'){
    exec_model=model_Path_Surface
    exec_data=data_Path_Surface
    exec_output=out_Path_Surface
}else{
    exec_model=model_Path_mouse
    exec_data=data_Path_mouse
    exec_output=out_Path_mouse    
}


#wet_model<-readRDS(file="C:/Users/k/Documents/test/6_weatherpredictmodel3.2")
#wet_test2<-read.delim("C:/Users/k/Documents/test/7_input_for_predict_tanna.csv",sep=",",stringsAsFactors = T,header = T)

wet_model<-readRDS(file=exec_model)
wet_test2<-read.delim(exec_data,sep=",",stringsAsFactors = T,header = T)

wet_test2

result2<-predict(wet_model,wet_test2)
#table(result2,wet_test2$judge)

Sys.time()
result2

outStr <-merge(Sys.time() , result2)

outStr

#write.csv(result2,"C:/Users/k/Documents/test/7_SVM_result.csv")
#write.csv(outStr,exec_output,append=TRUE)
write.table(outStr,exec_output,append=TRUE,sep=",",row.names=FALSE,col.names=FALSE)
