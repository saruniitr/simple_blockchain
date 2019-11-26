FROM python:3
RUN mkdir /usr/src/server
WORKDIR /usr/src/server
COPY requirements.txt /usr/src/server
RUN pip install -r requirements.txt
COPY . /usr/src/server
EXPOSE 5555
CMD [ "python", "./block_server.py" ]
