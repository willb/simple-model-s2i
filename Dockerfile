FROM radanalyticsio/openshift-spark

USER root

ADD . /opt/sms

WORKDIR /opt/sms

RUN yum install -y python-pip \
 && pip install -r requirements.txt

RUN chmod 755 /opt/sms/app.py

USER 185

CMD ./run.sh
