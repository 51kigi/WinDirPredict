#サンプルっぽい
#https://qiita.com/kazuki_hayakawa/items/18b7017da9a6f73eba77
#  http://www.turbare.net/transl/scipy-lecture-notes/packages/scikit-learn/index.html
#http://momijiame.tumblr.com/post/114751531866/python-iris-%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%E3%82%92%E3%82%B5%E3%83%9D%E3%83%BC%E3%83%88%E3%83%99%E3%82%AF%E3%82%BF%E3%83%BC%E3%83%9E%E3%82%B7%E3%83%B3%E3%81%A7%E5%88%86%E9%A1%9E%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B
#https://qiita.com/rennnosuke/items/fab837825b64bf50be56

#サンプル切り替え
#https://qiita.com/kotaroito/items/4eb29d42d7f8c534332f
#検証
#https://qiita.com/tomov3/items/039d4271ed30490edf7b

#  SVM関連
#http://neuro-educator.com/ml3/
#https://algorithm.joho.info/machine-learning/python-scikit-learn-nyumon/
#https://blog.excite.co.jp/exdev/28958132/
#http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
#http://scikit-learn.org/stable/modules/generated/sklearn.kernel_ridge.KernelRidge.html
#https://qiita.com/ynakayama/items/9c5867b6947aa41e9229

#並列化？crossvalidation?
#http://may46onez.hatenablog.com/entry/2016/02/19/152532
#https://qiita.com/yhyhyhjp/items/c81f7cea72a44a7bfd3a

#pandas
#https://pythondatascience.plavox.info/pandas/%E8%A1%8C%E3%83%BB%E5%88%97%E3%81%AE%E6%8A%BD%E5%87%BA
#https://pythondatascience.plavox.info/pandas/csv%e3%83%95%e3%82%a1%e3%82%a4%e3%83%ab%e3%81%ae%e8%aa%ad%e3%81%bf%e8%be%bc%e3%81%bf
# https://note.nkmk.me/python-pandas-read-csv-tsv/

#表示形式
#https://qiita.com/mas9612/items/af6a3030f9ef19feae22

#   以下は直接関係ないリンク
#http://d.hatena.ne.jp/n_shuyo/20100528/kernel_pca
#https://pepese.github.io/blog/python-ml-svm-multiclass/

#大きな流れ
#１、ファイルを読み込む
#２、結果と原因のデータセットに分ける
#３、学習する
#４、モデルを書き出す

#estimatorをSGDで試す(sklearnのチートシートによるとこれが良いらしい)
#http://neuro-educator.com/mlearn1/
#http://sinhrks.hatenablog.com/entry/2014/11/24/205305

if __name__=='__main__':
    import numpy as np
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    from sklearn import datasets
    from sklearn import svm
    from sklearn import multiclass
    from sklearn import metrics
    #from sklearn.cross_validation import train_test_split　　'depreciated
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import classification_report
    #from sklearn.grid_search import GridSearchCV 'depreciated
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    #モデルの切り替え時
    from sklearn.linear_model import LogisticRegression
    from sklearn.kernel_ridge import KernelRidge
    from sklearn import linear_model, metrics, preprocessing, cross_validation
    #富士通PCでインストールができなかったので以下をコメントアウト
    #from mlxtend.plotting import plot_decision_regions

    import pickle
    from sklearn.metrics import accuracy_score

    result_output_txt_path='./model/result_SGD.txt'

    print('modeling start')
    d=datetime.datetime.today()
    print('laptime:',d)

    with open (result_output_txt_path,"w") as f:
        f.write('modeling start' + "\n")
        f.write(str(d) + "\n")

    dataset_org=pd.read_csv("../data/5_reduced_united_test3.5.csv")
    X=dataset_org.iloc[:,0:6]
    Y=dataset_org.iloc[:,6]

    #標準化してしまう
    sc=StandardScaler()
    sc.fit(X)
    X_std=sc.transform(X)   
    
    clf= linear_model.SGDClassifier(loss="log",n_jobs=-1,shuffle=True)
    clf_result=clf.fit(X_std,Y)
    print(repr(clf_result))

    #交差検証
    scores=cross_validation.cross_val_score(clf_result,X_std,Y,cv=10)
    print("平均正解率=",scores.mean())
    print("正解率の標準偏差",scores.std())

    print('split test')
    d=datetime.datetime.today()
    print('laptime:',d)

    #データ分割して実行してみる
    X_train,X_test,Y_train,Y_test=train_test_split(X_std,Y,test_size=0.3,random_state=None)
    model_sgd= linear_model.SGDClassifier(loss="log",n_jobs=-1,shuffle=True)
    model_sgd.fit(X_train,Y_train)

    pred_train=model_sgd.predict(X_train)
    accuracy_train=accuracy_score(Y_train,pred_train)
    print('トレーニングデータに対する正解率 SGD　%.2f' % accuracy_train)

    pred_test=model_sgd.predict(X_test)
    accuracy_test=accuracy_score(Y_test,pred_test)
    print('テストデータに対する正解率　SGD:%.2f' % accuracy_test) 

    with open(result_output_txt_path,"a") as f:
         f.write("平均正解率=" + repr(scores.mean()) + '\n')
         f.write("正解率の標準偏差" + repr(scores.std()) + '\n')
         f.write(repr('トレーニングデータに対する正解率 SGD　%.2f' % accuracy_train) + '\n')
         f.write(repr('テストデータに対する正解率　SGD:%.2f' % accuracy_test )+ '\n')

    dict_westspd={10:0,12:0,14:0,16:2,20:0,22:0,24:0,26:0.5}
    dict_westonly={10:0,12:0,14:0,16:2,20:0,22:0,24:0,26:2}
    dict_allspd={10:1,12:1,14:1,16:2,20:0.5,22:0.5,24:0.5,26:0.5}
    
    clf_westspd= linear_model.SGDClassifier(loss="log",n_jobs=-1,shuffle=True,class_weight=dict_westspd)
    clf_westspd_result=clf.fit(X_std,Y)
    print(repr(clf_westspd_result))
    #交差検証westspd
    scores_westspd=cross_validation.cross_val_score(clf_westspd_result,X_std,Y,cv=10)
    print("平均正解率(westspd)=",scores_westspd.mean())
    print("正解率の標準偏差(westspd)",scores_westspd.std())

    clf_westonly= linear_model.SGDClassifier(loss="log",n_jobs=-1,shuffle=True,class_weight=dict_westonly)
    clf_westonly_result=clf.fit(X_std,Y)
    print(repr(clf_westonly_result))
    #交差検証westonly
    scores_westonly=cross_validation.cross_val_score(clf_westonly_result,X_std,Y,cv=10)
    print("平均正解率(westonly)=",scores_westonly.mean())
    print("正解率の標準偏差(westonly)",scores_westonly.std())

    clf_allspd= linear_model.SGDClassifier(loss="log",n_jobs=-1,shuffle=True,class_weight=dict_allspd)
    clf_allspd_result=clf.fit(X_std,Y)
    print(repr(clf_allspd_result))
    #交差検証allspd
    scores_allspd=cross_validation.cross_val_score(clf_allspd_result,X_std,Y,cv=10)
    print("平均正解率(allspd)=",scores_allspd.mean())
    print("正解率の標準偏差(allspd)",scores_allspd.std())


    with open(result_output_txt_path,"a") as f:
         f.write("平均正解率(westspd)=" + repr(scores_westspd.mean()) + '\n')
         f.write("正解率の標準偏差(westspd)" + repr(scores_westspd.std()) + '\n')
         f.write("平均正解率(westonly)=" + repr(scores_westonly.mean()) + '\n')
         f.write("正解率の標準偏差(westonly)" + repr(scores_westonly.std()) + '\n')
         f.write("平均正解率(allspd)=" + repr(scores_allspd.mean()) + '\n')
         f.write("正解率の標準偏差(allspd)" + repr(scores_allspd.std()) + '\n')

    print('set parameter for gridsearch')
    d=datetime.datetime.today()
    print('laptime:',d)

    #SGDのパラメータの最適をグリッドサーチで探してみる
    tuned_parameter=[
        {'loss':['hinge','log','modified_huber','squared_hinge','perceptron','squared_loss','huber'],
        'penalty':['none','l2','l1','elasticnet'],
        'alpha':[0.0001,0.001,0.01],
        'max_iter':[10,100,1000],
        'learning_rate':['constant','optimal','invscaling'],
        'eta0':[0.001,0.01,0.1,1.0,10.0],
        'class_weight':[dict_westspd,dict_westonly,dict_allspd]
        }
    ]

#epsilon_insentive,squred_epsilon_insentiveはサポートされないエラーが出たので外してみる
#eta0は0入れちゃダメだった
#'loss':['hinge','log','modified_huber','squared_hinge','perceptron','squared_loss','huber','epsilon_insentive','squred_epsilon_insentive'],

    score='f1'
    clf_gs_sgd=linear_model.SGDClassifier()
    clf_gs=GridSearchCV(
        clf_gs_sgd,
        tuned_parameter,
        cv=5,
        scoring='%s_weighted' % score,
        n_jobs=-1
    )

    print('start gridsearch fit')
    d=datetime.datetime.today()
    print('laptime:',d)
    
    clf_gs.fit(X_std,Y)

    print('グリッドサーチ結果')
    print(clf_gs.cv_results_)
    print('グリッドサーチ最適値')
    print(clf_gs.best_params_)
    print('best_estimator')
    print(clf_gs.best_estimator_)
    d=datetime.datetime.today()
    print('laptime:',d)

    with open(result_output_txt_path,"a") as f:
        f.write('グリッドサーチ結果' + "\n")
        f.write(repr(clf_gs.cv_results_) + "\n")
        f.write('グリッドサーチ最適値'  + "\n")
        f.write(repr(clf_gs.best_params_) + "\n")
        f.write('best_estimator' + "\n")
        f.write(repr(clf_gs.best_estimator_) + "\n")




#     tuned_parameters=[
 
#         {'C':[1,10,100,1000],'kernel':['rbf'],'gamma':[0.001,0.0001]},

#     ]
# #        {'C':[1,10,100,1000],'gamma':[0.001,0.0001]},
# #        {'C':[1,10,100,1000],'kernel':['linear']},
# #        {'C':[1,10,100,1000],'kernel':['rbf'],'gamma':[0.001,0.0001]},
# #        {'C':[1,10,100,1000],'kernel':['poly'],'degree':[2,3,4],'gamma':[0.001,0.0001]},
# #        {'C':[1,10,100,1000],'kernel':['sigmoid'],'gamma':[0.001,0.0001]}
# #   d=datetime.datetime.today()
# #   print('laptime:',d)

#     score='f1'
#     clf=GridSearchCV(
#         SVC(),
#         tuned_parameters,
#         cv=5,
#         scoring='%s_weighted' % score,
#         n_jobs=-1
#     )
#     #n_jobs=-1でCPUを自動調整で使用してくれるが、Windowsの場合は
#     #main loopを守るようなコーディングをしなければならないそうな、、、
#     d=datetime.datetime.today()
#     print('## start gridsearch.fit')
#     print('laptime:',d)

#     clf.fit(X_train,Y_train)
#     print('グリッドサーチ結果')
#     print(clf.cv_results_)
#     print('グリッドサーチ最適値')
#     print(clf.best_params_)
#     print('best_estimator')
#     print(clf.best_estimator_)
#     d=datetime.datetime.today()
#     print('laptime:',d)

#     with open(result_output_txt_path,"a") as f:
#         f.write('グリッドサーチ結果' + "\n")
#         f.write(repr(clf.cv_results_) + "\n")
#         f.write('グリッドサーチ最適値'  + "\n")
#         f.write(clf.best_params_ + "\n")
#         f.write('best_estimator' + "\n")
#         f.write(clf.best_estimator_ + "\n")

#     # それぞれのパラメータでの試行結果の表示
#     d=datetime.datetime.today()
#     print('laptime:',d)
#     print("Grid scores on development set:")
    
#     means=clf.cv_results_['mean_test_score']
#     stds=clf.cv_results_['std_test_score']

#     for means, std, params in zip(means,stds,clf.cv_results_['params']):
#         print("%0.3f (+/-%0.03f) for %r"
#             % (means, std * 2, params))
#     print()

#     # テストデータセットでの分類精度を表示
#     d=datetime.datetime.today()
#     print('laptime:',d)
#     print("The scores are computed on the full evaluation set.")
#     print()
#     y_true, y_pred = Y_test, clf.predict(X_test)
#     print(classification_report(y_true, y_pred))

#     #モデルの保存
#     d=datetime.datetime.today()
#     print('laptime:',d)
#     print('start saving model')
#     pickle.dump(model,open('./model/6_weather_predict_model_py_3.6','wb'))
#     pickle.dump(model_LR,open('./model/6_weather_predict_model_LR_py_3.6','wb'))

#     d=datetime.datetime.today()
#     print('laptime:',d)
#     print('end all process')

#     #モデルをファイルから読み出すとき
#         #loaded_model=pickle.load(open(filename,'rb'))
#         #pred_train=loaded_model.predict(X_train_std)
