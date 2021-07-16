FROM python:3.9-slim-buster

WORKDIR /workdir

COPY requirements.txt /workdir
RUN pip install -r requirements.txt

COPY server.py /workdir

CMD /workdir/server.py
