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
     
        print(response)
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


def formatResults(responseData, testData):

    message = ""

    # check if there were any instances of the test that failed
    if responseData['fails']:
        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: fail\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        message += "actualResult: ['successes': " + str(responseData['successes']) + " ['fails': " + str(responseData['successes']) + "\n"
        message += "moves: " + str(responseData['moves']) + "\n"

    else:
        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: success\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        # message += "actualResult: " + str(response['move']) + "\n"
        message += "moves: " + str(responseData['moves']) + "\n"

    with open(resultFileName, "a") as file:

        file.write(message)


def processResponse(response, responseData, testData):

    # check if the returned move is in the list of acceptable moves for the case
    if response['move'] in testData['expectedResult']:

        responseData["successes"] += 1

    else:

        responseData["fails"] += 1

    responseData["moves"][response['move']] += 1

    # return responseData


def main():

    testCasesFilePath = "testcases/testcases.json"

    #parse input arguments -m, method, -l, limit
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--path', help='path to testcases file')
    args = parser.parse_args()
    
    if args.path: 
        testCasesFilePath = args.path

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

                # Loop through the test according to the number of runs indicated
                while (testLoopCount <= test["turns"]):

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
                formatResults(responseData, test)

if __name__ == '__main__':
    main()