# WinDirPredict

Try to predict Tanna wind direction

## 背景 Background

GPVやWindy各種ニュースで風向予測がでるものの、別のアプローチで特定個所の予測ができないものか  
つまり、パラグライダーで飛ぶのにとりあえず丹那の3時間後の風向風力を予測したい、が動機

I know there are lot of usefule web site such as  
GPV,Windy and so on.
But, I just want to know wind direction of Tanna, next 3hours. So, I decide to make another way to predict.

### 概要 Description

* 入力は網代、三島のアメダスと丹那の風データ
* データの収集、整形、モデル作成と作ったモデルに現在の値をいれて3時間後を予測するツール  

* Input Amedas data(Ajiro,Mishima) and Tanna Wind data.
* Create some model to predict Tanna wind direction in 3hr.

### 実施内容 Tasks

丹那とその周辺の風はそれなりに関連性があるのでは？と仮定  
丹那及びアメダスのデータと3時間後の丹那のデータを並べて教師データを作成し  
学習したモデルを作成する

1. データの収集

    1. 丹那風情報の収集
        1. WindDatabaseから風情報をできるだけたくさん集める
        2. いらないカラムを削除して整形
    1. 周辺のデータを収集する
        1. 丹那を中心に東西にある三島と網代のアメダスデータを収集（CSVでざっくり落とす）
        2. 丹那の時と同様に要らないカラムを削除して整形
    1. 丹那データとアメダスデータを結合
    	1. 丹那データとアメダスデータを結合。アメダスデータは10分毎、丹那データは3分程度ごとなのでうまく調整しながら結合
    	2. 丹那の3時間後を上記のデータの横に結合
    	3. 3時間後の丹那データの値から判定結果をつける(風向と風力からラベルを付ける）

#### リンク Reffered Link

<http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html>
<https://qiita.com/oreo/items/82183bfbaac69971917f>
<https://qiita.com/yhyhyhjp/items/c81f7cea72a44a7bfd3a>
<https://pythondatascience.plavox.info/pandas/pandasのデータフレームに行や列を追加する>
<https://pythondatascience.plavox.info/pandas/データフレームを出力する>
<https://blog.amedama.jp/entry/2017/09/05/221037>
<http://programming-study.com/technology/python-if-main/>
<https://pythonhosted.org/joblib/parallel.html>
<http://datalove.hatenadiary.jp/entry/how-to-resolve-f-score-ill-defined-error>