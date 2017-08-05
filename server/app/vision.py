def pretty(d, indent=1):
    out = ""
    for key, value in d.items():
        out += ('\n' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            out += ('\n' * (indent+1) + str(value))
    return out

def ocr(url):
    ########### Optical Character Recognition (OCR) with Computer Vision API Using Python #############
    import http.client, urllib.request, urllib.parse, urllib.error, base64, json

    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '44b27428b9ba42a39f53e0915a56df94'

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'westus.api.cognitive.microsoft.com'

    headers = {
        # Request headers.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    # The URL of a JPEG image containing text.
    body = "{'url':'" + url + "'}"

    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
    except:
        text_output = "Error: Connection Request Fail"
        conn.close()
    try:
        data = response.read())
        dic = json.loads(data)
        text_output = ""
        for region in dic["regions"]:
            for line in region["lines"]:
                for word in line["words"]:
                    text_output += word["text"] + " "
                    # print(word["text"])
        # print(text_output)
    except Exception as e:
        print('Error:')
        print(e)
        # text_output = "error"
        conn.close()

    ####################################

    return text_output

def text_recognition(url):
    ########### Python 3.6 #############
    import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json

    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '44b27428b9ba42a39f53e0915a56df94'

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'https://westus.api.cognitive.microsoft.com'

    requestHeaders = {
        # Request headers.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # The URL of a JPEG image containing handwritten text.
    body = {'url' : url}

    # For printed text, set "handwriting" to false.
    params = {'handwriting' : 'true'}

    try:
        # This operation requrires two REST API calls. One to submit the image for processing,
        # the other to retrieve the text found in the image.
        #
        # This executes the first REST API call and gets the response.
        response = requests.request('POST', uri_base + '/vision/v1.0/RecognizeText', json=body, data=None, headers=requestHeaders, params=params)

        # Success is indicated by a status of 202.
        if response.status_code != 202:
            # if the first REST API call was not successful, display JSON data and exit.
            parsed = json.loads(response.text)
            print ("Error:")
            print (json.dumps(parsed, sort_keys=True, indent=2))
            exit()

        # The 'Operation-Location' in the response contains the URI to retrieve the recognized text.
        operationLocation = response.headers['Operation-Location']

        # Note: The response may not be immediately available. Handwriting recognition is an
        # async operation that can take a variable amount of time depending on the length
        # of the text you want to recognize. You may need to wait or retry this GET operation.

        print('\nHandwritten text submitted. Waiting 10 seconds to retrieve the recognized text.\n')
        time.sleep(10)

        # Execute the second REST API call and get the response.
        response = requests.request('GET', operationLocation, json=None, data=None, headers=requestHeaders, params=None)

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(response.text)
        print ("Response:")
        print (json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)

    ####################################

    return text_output
