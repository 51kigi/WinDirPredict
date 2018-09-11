import urllib
# If you are using Python 3+, import urllib instead of urllib2
import urllib.request
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
                    "Values": [ [ "248", "52", "180", "27", "196", "36", "value" ],  ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e7c5f40055d142f097c7c3fb93726e87/services/ddca418b04334abeb671b852c7b449dc/execute?api-version=2.0&details=true'
api_key = 'B0RcJQs5uWc5/+CwbTB4ih2bN2BbpwUfSUztyTOHxexpveACebgFltTf4wkbkBKXhFD92h9F+2k5U11O2/GkTg==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers) 

try:
    response = urllib.request.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    response = urllib.request.urlopen(req)
    result_dict=json.loads(response.read().decode('utf-8'))
    print(result_dict)
    print(result_dict['Results']['output1']['value']['Values'])
    north_prob=result_dict['Results']['output1']['value']['Values'][0][8]
    east_prob=result_dict['Results']['output1']['value']['Values'][0][7]
    south_prob=result_dict['Results']['output1']['value']['Values'][0][9]
    west_prob=result_dict['Results']['output1']['value']['Values'][0][10]
    tmp_pred=result_dict['Results']['output1']['value']['Values'][0][11]

    print(result_dict['Results']['output1']['value']['Values'][0][8])
    print(result_dict['Results']['output1']['value']['Values'][0][7])
    print(result_dict['Results']['output1']['value']['Values'][0][9])
    print(result_dict['Results']['output1']['value']['Values'][0][10])
    print(result_dict['Results']['output1']['value']['Values'][0][11]) 

    x_name=['North','East','South','West']
    y_value=[round(float(north_prob),3),round(float(east_prob),3),round(float(south_prob),3),round(float(west_prob),3)]
    
    JST = timezone(timedelta(hours=+9), 'JST')
    jst_now=datetime.datetime.now(JST)
    systimed="{0:%Y/%m/%d %H:%M}".format(jst_now)

    plt.title('4class neural')
    plt.bar(x_name,y_value)
    plt.xlabel('predicted at ' + systimed)
    plt.show()

    tmp_list=result_dict['Results']['output1']['value']['Values']
    tmp_list.insert(0,systimed)
    tmp_list.insert(1,'4classneural')
    tmp_list.insert(2,tmp_pred)

    print(tmp_list)

except  urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(e.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(e.info())

    print(json.loads(e.read()))                 
