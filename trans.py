import googletrans
import requests
import uuid
import json
def translate(text,src,dist):
    # Add your key and endpoint
    key = "6WzMtyS9kDrg6cUJuTEBVciTuAemYHTvhnMuXBRyq3rsDgEuPt1LJQQJ99BEAC3pKaRXJ3w3AAAbACOGVgOU"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    location = "eastasia"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': src,
        'to': dist
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params,
                            headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']
