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

if __name__=='__main__':
    import numpy as np
    import pandas as pd
    import datetime
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

    import pickle
    from sklearn.metrics import accuracy_score

    print('modeling start')
    d=datetime.datetime.today()
    print('d:',d)


    dataset_org=pd.read_csv("../data/test_set_tanna3.5.csv")
    X=dataset_org.iloc[:,0:6]
    Y=dataset_org.iloc[:,6]

    #データ分割
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=None)
    #データ標準化
    sc=StandardScaler()
    sc.fit(X_train)
    X_train_std=sc.transform(X_train)
    X_test_std=sc.transform(X_test)
    #学習
    #SVM
    #model=SVC(kernel='linear',random_state=None)
    model=SVC(kernel='rbf',random_state=None)
    model.fit(X_train_std,Y_train)
    #LogisticRegression
    model_LR=LogisticRegression(random_state=None)
    model_LR.fit(X_train_std,Y_train)
    #KernelRidge(array is too bigのエラーが出るので後回し)
    #model_KR=KernelRidge(alpha=1.0,kernel='rbf')
    #model_KR.fit(X_train_std,Y_train)

    d=datetime.datetime.today()
    print('d:',d)

    #以下は精度テスト
    pred_train=model.predict(X_train_std)
    accuracy_train=accuracy_score(Y_train,pred_train)
    print('トレーニングデータに対する正解率 SVM　%.2f' % accuracy_train)

    pred_train=model_LR.predict(X_train_std)
    accuracy_train=accuracy_score(Y_train,pred_train)
    print('トレーニングデータに対する正解率 LogisticRegression　%.2f' % accuracy_train)

    #pred_train=model_KR.predict(X_train_std)
    #accuracy_train=accuracy_score(Y_train,pred_train)
    #print('トレーニングデータに対する正解率 KernelRidge　%.2f' % accuracy_train)

    #pred_test=loaded_model.predict(X_test_std)
    pred_test=model.predict(X_test_std)
    accuracy_test=accuracy_score(Y_test,pred_test)
    print('テストデータに対する正解率　SVM:%.2f' % accuracy_test)

    pred_test=model_LR.predict(X_test_std)
    accuracy_test=accuracy_score(Y_test,pred_test)
    print('テストデータに対する正解率　LogisticRegression:%.2f' % accuracy_test)

    #pred_test=model_KR.predict(X_test_std)
    #accuracy_test=accuracy_score(Y_test,pred_test)
    #print('テストデータに対する正解率　KernelRidge:%.2' % accuracy_test)

    d=datetime.datetime.today()
    print('d:',d)

    scores=cross_val_score(model,X,Y)
    print('交差検証スコア　SVM:{}'.format(scores))
    print('平均スコア SVM:{}'.format(np.mean(scores)))

    scores=cross_val_score(model,X_test_std,Y_test)
    print('交差検証スコア　SVM_test: {}'.format(scores))
    print('平均スコア SVM_test:{}'.format(np.mean(scores)))

    d=datetime.datetime.today()
    print('d:',d)

    scores_LR=cross_val_score(model_LR,X,Y)
    print('交差検証スコア　LogisticRegression: {}'.format(scores_LR))
    print('平均スコア LogisticRegression:{}'.format(np.mean(scores_LR)))

    d=datetime.datetime.today()
    print('d:',d)

    #ちょっとグリッドサーチ
    #svm rbfカーネル のバンド幅(gamma)正則化パラメータ(c)について実施

    ##gridsearchのテストのためいったんスキップする
    #param_list=[0.001,0.01,0.1,1,10,100]
    #best_score=0
    #best_parameters={}
    #for gamma in param_list:
    #    for C in param_list:
    #        svm=SVC(gamma=gamma,C=C)
    #        svm.fit(X_train,Y_train)
    #        score=svm.score(X_test,Y_test)
    #        print('C:{}'.format(C))
    #        print('gamma:{}'.format(gamma))
    #        if score > best_score:
    #            print('change best')
    #            best_score=score
    #            best_parameters={'gamma':gamma,'C':C}
    #print('ベストスコア :{}'.format(best_score))
    #print('ベストパラメータ:{}'.format(best_parameters))
    d=datetime.datetime.today()
    print('## gridsearch set parameter')
    print('d:',d)

    tuned_parameters=[
        {'C':[1,10,100]},
    ]

#        {'C':[1,10,100,1000],'kernel':['rbf'],'gamma':[0.001,0.0001]},
#        {'C':[1,10,100,1000],'kernel':['poly'],'degree':[2,3,4],'gamma':[0.001,0.0001]},
#        {'C':[1,10,100,1000],'kernel':['sigmoid'],'gamma':[0.001,0.0001]}

    d=datetime.datetime.today()
    print('d:',d)

    score='f1'
    clf=GridSearchCV(
        SVC(),
        tuned_parameters,
        cv=5,
        scoring='%s_weighted' % score,
        n_jobs=-1
    )
    #n_jobs=-1でCPUを自動調整で使用してくれるが、Windowsの場合は
    #main loopを守るようなコーディングをしなければならないそうな、、、
    d=datetime.datetime.today()
    print('## start gridsearch.fit')
    print('d:',d)

    clf.fit(X_train,Y_train)
    print('グリッドサーチ結果')
    print(clf.cv_results_)
    print('グリッドサーチ最適値')
    print(clf.best_params_)
    print('best_estimator')
    print(clf.best_estimator_)

    # それぞれのパラメータでの試行結果の表示
    d=datetime.datetime.today()
    print('d:',d)
    print("Grid scores on development set:")
    
    means=clf.cv_results_['mean_test_score']
    stds=clf.cv_results_['std_test_score']

    for means, std, params in zip(means,stds,clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
            % (means, std * 2, params))
    print()

    # テストデータセットでの分類精度を表示
    d=datetime.datetime.today()
    print('d:',d)
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = Y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))

    #モデルの保存
    d=datetime.datetime.today()
    print('d:',d)
    print('start saving model')
    pickle.dump(model,open('./model/6_weather_predict_model_py_3.6','wb'))
    pickle.dump(model_LR,open('./model/6_weather_predict_model_LR_py_3.6','wb'))

    d=datetime.datetime.today()
    print('d:',d)
    print('end all process')

    #モデルをファイルから読み出すとき
        #loaded_model=pickle.load(open(filename,'rb'))
        #pred_train=loaded_model.predict(X_train_std)
