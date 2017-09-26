import base64
import requests
import cloudpickle

def publish(baseurl, validator, predictor):
    val = base64.b64encode(cloudpickle.dumps(validator))
    pred = base64.b64encode(cloudpickle.dumps(predictor))
    payload = {'validator' : val, 'predictor': pred}
    r = requests.post(baseurl + "/model", data=payload)
    return r.text

def predict(baseurl, args):
    payload = {'args': base64.b64encode(cloudpickle.dumps(args))}
    r = requests.post(baseurl + "/model", data=payload)
    return r.text

