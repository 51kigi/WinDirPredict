import urllib
import urllib.request
# If you are using Python 3+, import urllib instead of urllib2

import json 
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timezone,timedelta

data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["mishima_dir", "mishima_speed", "aziro_dir", "aziro_speed", "tannna_dir", "tanna_speed", "judge"],
                    "Values": [ [ "337", "17", "0", "19", "96", "50", "value" ],  ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e7c5f40055d142f097c7c3fb93726e87/services/030384f576904997984e7f71b7f990ae/execute?api-version=2.0&details=true'
api_key = 'KERUZzYKcZsrIn7vRhvNfl89xYEvmA/TQMZEltmlVEw72dw2EdIrbHQjNXE/pmkhZ4MhUyOlchiL3+DBmNk4JA==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

#req = urllib2.Request(url, body, headers) 
req = urllib.request.Request(url, body, headers)
try:
    #response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    #response = urllib.request.urlopen(req)

    response = urllib.request.urlopen(req)
    result_dict=json.loads(response.read().decode('utf-8'))
    print (result_dict)
    for res in result_dict:
        print(res)

    print(result_dict['Results']['output1']['value']['Values'])

    tmp_pred=str(result_dict['Results']['output1']['value']['Values'][0][7])
    # tmp_pred='North'

    x_name=[tmp_pred,'not'+tmp_pred]
    y=result_dict['Results']['output1']['value']['Values'][0][8]
    y_value=(float(y),1.0-float(y))
    y_value_2=np.array(y_value)
    print(type(x_name))
    print(x_name)
    print(type(y))
    print(y)
    print(type(y_value))
    print(y_value)
    print(type(y_value_2))
    print(y_value_2)

    plt.title("2class deci tree")
    plt.bar(x_name,y_value)
    plt.show()
    #時刻取得
    JST = timezone(timedelta(hours=+9), 'JST')
    jst_now=datetime.datetime.now(JST)
    systimed="{0:%Y/%m/%d %H:%M}".format(jst_now)

    tmp_list=result_dict['Results']['output1']['value']['Values']
    tmp_list.insert(0,systimed)
    tmp_list.insert(1,'2classDeciTree')
    tmp_list.insert(2,tmp_pred)

    print(tmp_list)

    pred=tmp_pred

    #print(result_dict['Results']['output1']['value']['Values'][0][15]) 
    print(pred)
    #except urllib.HTTPError, error:
except urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(e.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(e.info())

    print(json.loads(e.read()))                 