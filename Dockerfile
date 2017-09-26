FROM centos:latest

USER root

ADD . /opt/sms

WORKDIR /opt/sms

RUN yum install -y python-pip \
 && pip install -r requirements.txt
 
USER 185

CMD ./run.sh
