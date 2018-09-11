import urllib
import urllib.request

#import urllib2
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
                    "Values": [ [ "0", "0", "0", "0", "0", "0", "value" ], [ "0", "0", "0", "0", "0", "0", "value" ], ]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e7c5f40055d142f097c7c3fb93726e87/services/0e4edaedd8b6475785932c9d6c7659cf/execute?api-version=2.0&details=true'
api_key = '4b7mfMOufa9ik4UOh8hGSEERXnjWlybwKajiC+jHZN75WjbKJZnJzzOs2MDAdqo3a2wKIHU6Gdv2OT/jiDUStA==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

#req = urllib2.Request(url, body, headers) 
req = urllib.request.Request(url, body, headers)

try:
    #response = urllib2.urlopen(req)
    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    response = urllib.request.urlopen(req)
    result_dict=json.loads(response.read().decode('utf-8'))
    tmp_pred=str(result_dict['Results']['output1']['value']['Values'][0][15])
    # tmp_pred='North'
    #pred=tmp_pred
    #result = response.read()
    print(result_dict['Results']['output1']['value']['Values'])
    north_prob=float(result_dict['Results']['output1']['value']['Values'][0][8])
    east_prob=float(result_dict['Results']['output1']['value']['Values'][0][7])
    south_prob=float(result_dict['Results']['output1']['value']['Values'][0][11])
    west_prob=float(result_dict['Results']['output1']['value']['Values'][0][14])
    
    snorth_prob=float(result_dict['Results']['output1']['value']['Values'][0][10])
    seast_prob=float(result_dict['Results']['output1']['value']['Values'][0][9])
    ssouth_prob=float(result_dict['Results']['output1']['value']['Values'][0][12])
    swest_prob=float(result_dict['Results']['output1']['value']['Values'][0][13])

    x_name=['North','East','South','West','StrongN','StrongE','StrongS','StrongW']
    y_value=[north_prob,east_prob,south_prob,west_prob,snorth_prob,seast_prob,ssouth_prob,swest_prob]

    JST = timezone(timedelta(hours=+9), 'JST')
    jst_now=datetime.datetime.now(JST)
    systimed="{0:%Y/%m/%d %H:%M}".format(jst_now)

    plt.title('8class LogReg')
    plt.bar(x_name,y_value)
    plt.xlabel('predicted at ' + systimed)
    plt.show()

    tmp_list=result_dict['Results']['output1']['value']['Values']
    tmp_list.insert(0,systimed)
    tmp_list.insert(1,'8classLogReg')
    tmp_list.insert(2,tmp_pred)

    print(tmp_list)


    print(pred) 
except urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(e.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(e.info())

    print(json.loads(e.read()))                 
