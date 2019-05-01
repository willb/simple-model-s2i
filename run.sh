#!/bin/bash

export S2I_MODEL_PATH=${S2I_MODEL_PATH:-/opt/sms/model.pickle}
exec /opt/sms/app/bin/uwsgi --http 0.0.0.0:8080 --wsgi-file /opt/sms/app.py --callable app_dispatch
