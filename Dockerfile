FROM python:3

ADD python_server .

CMD [ "python3", "server.py" ]
