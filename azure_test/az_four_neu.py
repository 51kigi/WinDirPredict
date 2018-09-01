import urllib
# If you are using Python 3+, import urllib instead of urllib2
import urllib.request
import json 


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

    print(result_dict['Results']['output1']['value']['Values'][0][11]) 

except  urllib.error.HTTPError as e:
    print("The request failed with status code: " + str(e.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(e.info())

    print(json.loads(e.read()))                 
