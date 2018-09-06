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

### 実施内容 Process

丹那とその周辺の風はそれなりに関連性があるのでは？と仮定

1. 丹那及びアメダスのデータと3時間後の丹那のデータを並べて教師データを作成し学習したモデルを作成する

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
    1. データの整形
        1. 出来上がった判定付きデータからモデルに投入する項目のみを抽出  
        上記のデータから3時間後の丹那データを削除（モデル作成時のパラメータにはならない）  
        後でモデルに投入するパラメータを増やしたくなる事があるので、  
        データの整形とモデルはセットにしておいたほうが良いかも。  
        途中でカラムを追加する場合でも最後が結果になるようにしておかないとモデルに  
        投入するときに設定が面倒になる

    1. モデルに投入(学習）
        1. R,Pythonともモデルに合わせてトレーニングを行う
        1. 出来上がったモデルの精度などを確認して、適当なものを保存する  
            後で予測する際に保存したモデルを読み込み、予測のためのパラメータの  
            投入と結果の取得ができるようにしておく
        1. 学習結果の保存  
        後で他のモデルと比較したくなるので精度に関する情報をこの段階で出力しておく  

    1. 予測処理に使用するデータの収集
        1. アメダスデータをHTMLからスクレイピングして取得  
            アメダスデータを返してくれるAPIが見つからなかったのでWebページからスクレイピングして取得
        1. 丹那データを取得  
            学習用データを取得した時と同じ手順で取得し、一番最後のデータのみを使用する  
            今回の方法では当日のデータを取得した際に当日1800までは取得できる。  
            1800以降に予測しようとしても丹那のパラメータは変化しないので、正しい予測は得られない  
            (1800以降飛ぶことはないと思われるので実質問題ないと判断）
        1. データを結合してファイル出力  
            同じインプットデータを複数のモデルで使用する予定なのでファイル出力しておく  
            使用方法により投入データの取得からモデルの投入を一連の流れで行うのが良い場合も

    1. モデルに投入し結果を取得
        1. 上記データをモデルに投入して結果を取得、確認

1. 学習したモデルを使用して現時点での予想をwebで返す
    1. 丹那風情報を取得
    1. アメダス情報を取得
    1. Pythonで作成したモデルに投入
    1. AzureMLで作成したモデルに投入
    1. モデルから取得した予測結果を表示  
    　　[WindDirPred](https://windpred.azurewebsites.net/) 

#### リンク Link

<https://jbt.github.io/markdown-editor/>
<http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html>
<https://qiita.com/oreo/items/82183bfbaac69971917f>
<https://qiita.com/yhyhyhjp/items/c81f7cea72a44a7bfd3a>
<https://pythondatascience.plavox.info/pandas/pandasのデータフレームに行や列を追加する>
<https://pythondatascience.plavox.info/pandas/データフレームを出力する>
<https://blog.amedama.jp/entry/2017/09/05/221037>
<http://programming-study.com/technology/python-if-main/>
<https://pythonhosted.org/joblib/parallel.html>
<http://datalove.hatenadiary.jp/entry/how-to-resolve-f-score-ill-defined-error>