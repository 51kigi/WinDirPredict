#import urllib2
import urllib
import urllib.request
# If you are using Python 3+, import urllib instead of urllib2

import json 


data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["userID"],
                    #"Values": [ [ "value" ], [ "value" ], ]
                    "Values":[["U1048"]]
                },        },
            "GlobalParameters": {
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e7c5f40055d142f097c7c3fb93726e87/services/779299b8b8e946229cdffef87fba146c/execute?api-version=2.0&details=true'
api_key = 'h3q1TqTFLMs2pqYgW16KopuQEFcJKO3X40FXqSP1bqqubnaqNpS1MKnptWGTocYSPXLvbfb3P8nvjN9AICSp9Q==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

#req = urllib2.Request(url, body, headers) 
#req = urllib.request.Request(url, body, headers) 
req=urllib.request.Request(url,body,headers)

try:
    #response = urllib2.urlopen(req)
    response=urllib.request.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
#except urllib2.HTTPError,error:
except urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))                 