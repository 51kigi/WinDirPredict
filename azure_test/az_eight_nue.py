import urllib
import urllib.request
# If you are using Python 3+, import urllib instead of urllib2

import json 


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

url = 'https://ussouthcentral.services.azureml.net/workspaces/e7c5f40055d142f097c7c3fb93726e87/services/18e7a8dcc94247389abc04eae6ed16cd/execute?api-version=2.0&details=true'
api_key = 'm/P3YXx2OcmO32pNo29uD9wdknTjiVqMpU4UDBwb43lm7boYohby8nWQk8AcflTysaQhztSKhOOJ06l1aBXEYA==' # Replace this with the API key for the web service
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
    tmp_pred=str(result_dict['Results']['output1']['value']['Values'][0][15])
    # tmp_pred='North'
    pred=tmp_pred

    if tmp_pred=='SNorth':
        pred='North Strong'
    elif tmp_pred=='SEast':
        pred='East Strong'
    elif tmp_pred=='SSouth':
        pred='South Strong'
    elif tmp_pred=='SWest':
        pred='West Strong'
    else:
        pred=tmp_pred




    #print(result_dict['Results']['output1']['value']['Values'][0][15]) 
    print(pred)
    #except urllib.HTTPError, error:
except urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(e.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(e.info())

    print(json.loads(e.read()))                 