from flask import Flask, redirect, request, url_for
import base64
from cPickle import loads as cPloads
import numpy

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
    if app.model is None:
        return "Install a model by POSTing to /model"
    else:
        return "Make a prediction by POSTing to /predict"

@app.route('/model', methods=['POST', 'GET'])
def new_model():
    error = None
    
    if request.method == 'POST':
        if app.model is not None:
            error = "Error:  You've already installed a model"
        elif 'validator' in request.form and 'predictor' in request.form:
            val = cPloads(base64.b64decode(request.form['validator']))
            pred = cPloads(base64.b64decode(request.form['predictor']))

            app.model = Model(val, pred)
        else:
            error = "Error:  I need a validator and a predictor"
    
    if error is not None:
        return error
    elif app.model is None:
        return "Install a model by POSTing to /model"
    else:
        return "Make a prediction by POSTing to /predict"

@app.route('/predict', methods=['POST'])
def predict():
    import json
    args = cPloads(base64.b64decode(request.form['args']))
    try:
        return json.dumps(app.model(args))
    except ValueError, ve:
        return str(ve)
    except Exception, e:
        print str(e)


if __name__ == '__main__':
    app.logger.setLevel(0)
    app.run(port=8080)
