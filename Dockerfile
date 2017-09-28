FROM radanalyticsio/openshift-spark

USER root

ADD . /opt/sms

WORKDIR /opt/sms

RUN yum install -y python-pip \
 && pip install -r requirements.txt

RUN chmod 755 /opt/sms/app.py

USER 185

LABEL io.k8s.description="Example model microservice." \
      io.k8s.display-name="simple-model-server" \
      io.openshift.expose-services="8080:http"

CMD ./run.sh
