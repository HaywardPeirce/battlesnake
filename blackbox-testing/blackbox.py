import requests, json, time

currentTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

resultFileName = "backbox_testing_result_" + currentTime + ".json"

testResults = {}

with open("testcases.json") as casesfile: 
    casesData = casesfile.read() 
    data_parsed = json.loads(casesData) 

    for test in data_parsed:
        
        with open(data_parsed[test].fileName) as file:  
            data = file.read() 
            data_parsed = json.loads(data) 
            print(data_parsed)
            
            try:
                testResponse = makeTestAPICall(data_parsed)
            except:
                print ("Error!")
            
            if testResponse:
                processResponse(testResponse, data_parsed)
                



def makeTestAPICall(data, url = 'http://localhost:8080', headers = {'Content-Type' : 'application/json'}):
    
    try:
        response = requests.post(url, headers = headers, data = data_parsed)
     
        print(response)
        response.raise_for_status()
    
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        # return errh
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        # return errc
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        # return errt
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        # return err
    
    return response.


def processResults(response, testData):
    
    print(response.move)
    
    message = {}
    
    # check if the returned move is in the list of acceptable moves for the case
    if response.move is in testData.expectedResult:
        
        message = {
            testData.name: {
                "status": "success",
                "expectedResult": testData.expectedResult,
                "actualResult":response.move
                
            }
        }
            
    else: 
        message = {
            testData.name: {
                "status": "fail",
                "expectedResult": testData.expectedResult,
                "actualResult":response.move
                
            }
        }
        
        
    with open(resultFileName, "a") as file:
            
        data = file.write(message)