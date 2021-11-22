import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc
import paho.mqtt.client as mqtt
import threading

history = list()

def on_message(client, obj, msg):
	history.append(int(msg.payload))
	print(history)
	print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")

### subscriber
class LogServicer(log_pb2_grpc.LogServicer):


	def Get(self, request, context):
		print("Receive GET at log server via gRPC ... ,", history)
		response = log_pb2.LogResponse()
		for h in history: response.data.append(h)
		return response
	

class Subscriber():
	def __init__(self):
		self.client = mqtt.Client()
		self.client.on_message = on_message
		self.client.connect(host="127.0.0.4", port=1883) ## docker port
		self.client.subscribe('his', 0) 
		
	def run(self):
		self.client.loop_forever()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--ip", default="127.0.0.1", type=str)
	parser.add_argument("--port", default=8082, type=int)
	args = vars(parser.parse_args())

	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	sub = Subscriber()
	servicer = LogServicer()
	log_pb2_grpc.add_LogServicer_to_server(servicer, server)

	t = threading.Thread(target=sub.run)

	try:
		server.add_insecure_port(f"{args['ip']}:{args['port']}")
		t.start()
		server.start()
		print(f"Run gRPC Log Server at {args['ip']}:{args['port']}")
		server.wait_for_termination()
	except KeyboardInterrupt:
		pass
