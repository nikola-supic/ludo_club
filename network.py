"""
Created on Wed Feb 24 21:17:20 2021

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
	def __init__(self, lobby_size):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = 'localhost'
		self.port = 5555
		self.addr = (self.server, self.port)
		self.p = self.connect(lobby_size)

	def get_p(self):
		return self.p

	def connect(self, lobby_size):
		print(f'[ > ] Trying to connect to: {self.server}:{self.port}')
		try:
			self.client.connect(self.addr)
			self.client.send(str.encode(str(lobby_size)))
			return self.client.recv(2048).decode()
		except:
			pass

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return pickle.loads(self.client.recv(2048*4))
		except socket.error as e:
			print(e)