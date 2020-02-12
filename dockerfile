FROM python:3.7.6

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD python /code/run.py
