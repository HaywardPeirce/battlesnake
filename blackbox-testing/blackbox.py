import requests, json
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


def processResponse(response, testData):
    
    # print(testData['expectedResult'])

    # expectedResult = json.loads(testData['expectedResult'])

    # print(expectedResult)

    # message = {}

    message = ""

    # check if the returned move is in the list of acceptable moves for the case
    if response['move'] in testData['expectedResult']:

        # message = {
        #     testData['name']: {
        #         "status": "success",
        #         "expectedResult": testData['expectedResult'],
        #         "actualResult": response['move']
        #
        #     }
        # }

        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: success\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        message += "actualResult: " + str(response['move']) + "\n"

    else:
        # message = {
        #     testData['name']: {
        #         "status": "fail",
        #         "expectedResult": testData['expectedResult'],
        #         "actualResult": response['move']
        #
        #     }
        # }
        message += "----------\n"
        message += "Test case: " + testData['name'] + "\n"
        message += "status: fail\n"
        message += "expectedResult: " + str(testData['expectedResult']) + "\n"
        message += "actualResult: " + str(response['move']) + "\n"


    with open(resultFileName, "a") as file:

        file.write(message)

def main():
    with open("testcases/testcases.json") as casesfile:
        casesData = casesfile.read()
        data_parsed = json.loads(casesData)

        for test in data_parsed:

            # print("test:{}".format(test))

            # print("test:{}".format(test[0]))
            print("test:{}".format(test["name"]))

            with open("testcases/" + test["fileName"]) as file:
                data = file.read()
                data_parsed = json.loads(data)
                # print("data_parsed".format(data_parsed))

                # print(type(data_parsed))
                try:
                    testResponse = makeTestAPICall(data_parsed)

                    # print("testResponse: {}".format(testResponse.content))

                    processResponse(json.loads(testResponse.content), test)

                except Exception as e:
                    print ("Error!: {}".format(e))



if __name__ == '__main__':
    main()