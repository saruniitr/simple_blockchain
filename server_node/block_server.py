import json
import logging
import os
import sys
import time
from uuid import uuid4
import zmq

logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

address = os.environ["ZMQ_BIND_ADDRESS"]
logging.info(f"Server bind Address: {address}")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(address)
server_id = uuid4().hex[:8]
logging.info("Starting server, Id: {}".format(server_id))
num_messages = 0

while True:
    logging.info(f"[{server_id}] Waiting for transactions ...")
    message = socket.recv()
    data = json.loads(message)
    logging.info(f"Received transaction: {data['id']}")
    num_messages += 1
    time.sleep(1)
    socket.send_string(f"[{server_id}] No. messages received: {num_messages}")
