def azureml_main(dataframe1=None,dataframe2=None):
    import pandas as pd
    import nltk
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import GridSearchCV

    from azureml import Workspace
    
    ws = Workspace(
        workspace_id='6c9e49ea0941429fb331f631799b27c9',
        authorization_token='YmyaeNEZvUT5qeyDRPNo3R0Rsf7bV3ZJ5LESPCjEY08wg+XlE9HppKw4Ia4o87kzbzVJzF84EBmj7rXmEGewGw==',
        endpoint='https://studioapi.azureml.net'
    )
    ds = ws.datasets['test_set_tanna3.5.csv']
    frame = ds.to_dataframe()

    X=frame.iloc[:,0:6]
    Y=frame.iloc[:,:6]

    #データ分割
    X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=None)

    tuned_parameters=[
        {'C':[1,10,100,1000],'kernel':['linear']},
        {'C':[1,10,100,1000],'kernel':['rbf'],'gamma':[0.001,0.0001]},
        {'C':[1,10,100,1000],'kernel':['poly'],'degree':[2,3,4],'gamma':[0.001,0.0001]},
        {'C':[1,10,100,1000],'kernel':['sigmoid'],'gamma':[0.001,0.0001]}
    ]

    d=datetime.datetime.today()
    print('d:',d)

    score='f1'
    clf=GridSearchCV(
        SVC(),
        tuned_parameters,
        cv=5,
        scoring='%s_weighted' % score,
        n_jobs=1
    )
    #n_jobs=-1でCPUを自動調整で使用してくれるが、Windowsの場合は
    #main loopを守るようなコーディングをしなければならないそうな、、、

    clf.fit(X_train,Y_train)
    print('グリッドサーチ結果')
    print(clf.grid_scores_)
    print('グリッドサーチ最適値')
    print(clf.best_params_)
    print('best_estimator')
    print(clf.best_estimator_)

    # それぞれのパラメータでの試行結果の表示
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
            % (mean_score, scores.std() * 2, params))
    print()

    # テストデータセットでの分類精度を表示
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = Y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))

