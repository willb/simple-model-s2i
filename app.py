from flask import Flask, redirect, request, url_for
import base64
from pickle import load as cPload
from pickle import loads as cPloads
import numpy
import cloudpickle
import sys
import os
import pandas as pd

app = Flask(__name__)

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
        predictions = app.model.predict(pd.DataFrame([args]))
        return json.dumps(predictions.tolist())
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
  try:
      import json
      from sklearn.pipeline import Pipeline
      app.model = Pipeline([(k, cPload(open(v, "rb"))) for k, v in json.load(open("stages.json", "r"))])
      
  except Exception as e:
    print(str(e))
    sys.exit()
  app.logger.setLevel(0)
  app.run(host='0.0.0.0', port=8080)
