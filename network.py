"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: network.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

import socket
import pickle
import json

class Network():
	def __init__(self, msg):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = 'localhost'
		self.port = 5555
		self.addr = (self.server, self.port)
		self.p = self.connect(msg)

	def get_p(self):
		return self.p

	def connect(self, msg):
		try:
			print(f'[ > ] Trying to connect to: {self.server}:{self.port}')
			self.client.connect(self.addr)
			self.client.send(str.encode(msg))
			return self.client.recv(2048).decode()
		except:
			print(f'[ > ] Error while trying connection to: {self.server}:{self.port}')

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return pickle.loads(self.client.recv(2048*4))
		except socket.error as e:
			print(e)