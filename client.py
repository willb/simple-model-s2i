import base64
import requests
import cloudpickle

def predict(baseurl, args):
    payload = {'args': base64.b64encode(cloudpickle.dumps(args))}
    r = requests.post(baseurl + "/predict", data=payload)
    return r.text

