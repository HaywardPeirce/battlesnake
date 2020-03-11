import requests, json, argparse
from datetime import datetime

currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

resultFileName = "backbox_testing_result_" + currentTime + ".txt"

testResults = {}

def makeTestAPICall(data, url = 'http://localhost:8080/move', headers = {"Content-Type" : "application/json"}):

    data = json.dumps(data)

    # print("data: {} {}".format(data, type(data)))


    try:
        response = requests.post(url, headers = headers, data = data)
     
        # print(response)
        response.raise_for_status()
    
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
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
    
    return response


def formatResults(responseData, testData, testMode):

    message = ""

    # check if there were any instances of the test that failed
    if responseData['fails'] and (testMode == "all" or testMode == "fail"):
        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: fail\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        message += "actualResult: ['successes': " + str(responseData['successes']) + "] ['fails': " + str(responseData['fails']) + "]\n"
        message += "moves: " + str(responseData['moves']) + "\n"

    elif responseData['successes'] and (testMode == "all" or testMode == "pass"):
        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: success\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        # message += "actualResult: " + str(response['move']) + "\n"
        message += "moves: " + str(responseData['moves']) + "\n"

    # check that there are results to print to the file
    if message:
        with open(resultFileName, "a") as file:
            
            file.write(message)


def processResponse(response, responseData, testData):

    # print(responseData)

    # check if the returned move is in the list of acceptable moves for the case
    if response['move'] in testData['expectedResult']:

        responseData["successes"] += 1

    else:

        responseData["fails"] += 1

    responseData["moves"][response['move']] += 1

    # return responseData


def main():

    testCasesFilePath = "testcases/testcases.json"
    testMode = "all"
    overrideRuns = False
    runCount = 1

    #parse input arguments -m, method, -l, limit
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', help='path to testcases file')
    parser.add_argument('-m','--mode', help='test case mode - all, pass, fail')
    parser.add_argument('-r','--runs', help='How many runs of each test to do. Overrides explicit numbers in config file')
    args = parser.parse_args()
    
    if args.path: 
        testCasesFilePath = args.path
    if args.mode: 
        testMode = args.mode
    if args.runs: 
        runCount = int(args.runs)
        overrideRuns = True

    with open(testCasesFilePath) as casesfile:
        casesData = casesfile.read()
        data_parsed = json.loads(casesData)

        for test in data_parsed:

            if test["enabled"]:

                # print("test:{}".format(test))

                testLoopCount = 0

                responseData = {
                    "successes": 0,
                    "fails": 0,
                    "moves":
                        {
                            "right": 0,
                            "left": 0,
                            "up": 0,
                            "down": 0
                        }
                    }

                # if a CLI override of the number of loops to do was included then use that, otherwise use the value from the file
                if overrideRuns:
                    temprunCount = runCount

                else:
                    temprunCount = test["turns"]

                # Loop through the test according to the number of runs indicated
                while (testLoopCount < temprunCount):

                    # print("test:{}".format(test[0]))
                    print("test:{}".format(test["name"]))

                    try:
                        with open("testcases/" + test["fileName"]) as file:
                            data = file.read()
                            data_parsed = json.loads(data)
                            # print("data_parsed".format(data_parsed))

                            # print(type(data_parsed))
                            try:
                                testResponse = makeTestAPICall(data_parsed)

                                # print("testResponse: {}".format(testResponse.content))

                                processResponse(json.loads(testResponse.content), responseData,  test)

                            except Exception as e:
                                print ("Error!: {}".format(e))
                    except Exception as e:
                        print ("Error!: {}".format(e))

                    testLoopCount += 1
                
                # Once all the test repetitions have been completed, format the results
                formatResults(responseData, test, testMode)

if __name__ == '__main__':
    main()