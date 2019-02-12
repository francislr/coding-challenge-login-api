FROM python:3
RUN mkdir -p /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY ./deployment/django/run /usr/bin/run-webapp
COPY ./deployment/django/manage /usr/bin/manage
RUN chmod 777 /usr/bin/run-webapp
RUN chmod 777 /usr/bin/manage
CMD /usr/bin/run-webapp

