#python用に書き直す予定


#http://d.hatena.ne.jp/hoxo_m/20110324/p1
#https://bi.biopapyrus.jp/ai/machine-learning/svm/r/
#http://www.cis.doshisha.ac.jp/mjin/R/31/31.html
# 実行方法
#事前にtest_set_tanna3.4.csvを作っておく(RedudcedSetの一部を切り出す）
#"C:\Program Files\R\R-3.4.3\bin\rscript.exe" 6_R_tanna_svm_script_v3.4.r 

#チューニング
#http://testblog234wfhb.blogspot.jp/2014/06/support-vector-machine-tuning-by-caret.html
#http://d.hatena.ne.jp/hoxo_m/20110325/p1
#http://cream-worker.blog.jp/archives/1070032623.html

Sys.time()
gc()
library(kernlab)
wet_train<-read.delim("C:/Users/k/Documents/test/reduced_united_test3.5.csv",sep=",",stringsAsFactors = T,header = T)
Sys.time()
wet_model<-ksvm(judge~.,data=wet_train,type="C-bsvc",kernel="rbfdot",gamma=0.1,C=10,cross=8)
Sys.time()
wet_test<-read.delim("C:/Users/k/Documents/test/test_set_tanna3.5.csv",sep=",",stringsAsFactors = T,header = T)
Sys.time()
result<-predict(wet_model,wet_test)
Sys.time()
saveRDS(wet_model,file="C:/Users/k/Documents/test/6_weatherpredictmodel3.6")
Sys.time()
table(result,wet_test$judge)
Sys.time()
write.csv(result,"C:/Users/k/Documents/test/6_SVM_result.csv")
Sys.time()
write.csv(table(result,wet_test$judge),"C:/Users/k/Documents/test/6_SVM_result_table.csv")
Sys.time()