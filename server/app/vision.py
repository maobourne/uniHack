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
        data = response.read()
    except:
        text_output = "Error: Connection Request Fail"
    try:
        text_output = json.parse(str(data))
        #text_output = text_output.text
        #text_output = parsed
        conn.close()

    except Exception as e:
        print('Error:')
        print(e)
        text_output = "error"

    ####################################

    return text_output
