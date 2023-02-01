FROM python:3

ADD python_server /

CMD [ "python", "server.py" ]
