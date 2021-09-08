FROM python:3.6.12-alpine3.12

ADD ./ /test
RUN chmod -R 755 /test

RUN apk --no-cache add --virtual=.build-dep build-base \
    && apk --no-cache add libzmq \
    && apk --no-cache add zeromq-dev libffi-dev \
    && apk --no-cache add curl \
    && apk --no-cache add jq \
    && pip3 install --no-cache-dir locust==1.5.3 \
    && apk del .build-dep \
    && chmod +x /test/docker-entrypoint.sh
RUN pip3 install flask
RUN pip3 install flask_restful
RUN pip3 install kubernetes==10.0.1
RUN pip3 install requests==2.22.0
RUN pip3 install json-logging==1.0.5
RUN  mkdir /locust
EXPOSE 8089 5557 5558 5005
ENV SCENARIO_FILE /test/locustfile.py
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["sh"]
CMD ["/test/docker-entrypoint.sh]
