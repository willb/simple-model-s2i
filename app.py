from flask import Flask, redirect, request, url_for
import base64
from pickle import load as cPload
from pickle import loads as cPloads
import numpy
import cloudpickle
import sys
import os

app = Flask(__name__)

class Model(object):
    def __init__(self, validator, predictor):
        self.validator = validator
        self.predictor = predictor
    def __call__(self, args):
        if self.validator(args):
            return self.predictor(args)
        else:
            raise ValueError("I don't know how to score the args (%r) you supplied" % args)

app.model = None

@app.route('/')
def index():
  return "Make a prediction by POSTing to /predict"

@app.route('/predict', methods=['POST'])
def predict():
    import json
    if 'json_args' in request.form:
      args = json.loads(request.form['json_args'])
    else:
      args = cPloads(base64.b64decode(request.form['args']))
    try:
        return json.dumps(app.model(args))
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
  try:
    with open(os.getenv("S2I_MODEL_PATH"), "rb") as f:
      (val, pred) = cPload(f)
      app.model = Model(val, pred)
  except Exception as e:
    print(str(e))
    sys.exit()
  app.logger.setLevel(0)
  app.run(host='0.0.0.0', port=8080)
