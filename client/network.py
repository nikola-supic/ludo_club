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

class Network():
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = '4.tcp.ngrok.io'
		self.port = 16203
		self.addr = (self.server, self.port)
		self.first_data = self.connect()
		print(f'[ + ] Successfully connected.')

	def get_first_data(self):
		return self.first_data

	def connect(self):
		try:
			print(f'[ > ] Trying connection to: {self.server}:{self.port}')
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except Exception as e:
			print(e)
			print(f'[ - ] Error while connecting to: {self.server}:{self.port}')

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return pickle.loads(self.client.recv(2048*4))
		except socket.error as e:
			print(e)