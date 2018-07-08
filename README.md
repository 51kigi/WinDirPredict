# WinDirPredict
Try to predict Tanna wind direction
# 背景 Background
GPVやWindy各種ニュースで風向予測がでるものの、別のアプローチで特定個所の予測ができないものか  
つまり、パラグライダーで飛ぶのにとりあえず丹那の3時間後の風向風力を予測したい、が動機

I know there are lot of usefule web site such as  
GPV,Windy and so on.
But, I just want to know wind direction of Tanna, next 3hours. So, I decide to make another way to predict.

# 概要 Description
* 入力は網代、三島のアメダスと丹那の風データ
* データの収集、整形、モデル作成と作ったモデルに現在の値をいれて3時間後を予測するツール  

* Input Amedas data(Ajiro,Mishima) and Tanna Wind data.
* Create some model to predict Tanna wind direction in 3hr.
# リンク Reffered Link
<http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html>
<https://qiita.com/oreo/items/82183bfbaac69971917f>
