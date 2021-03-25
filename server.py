"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: server.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

import socket
from _thread import start_new_thread
import pickle
import time
from datetime import datetime

from game import Game

class Server():
	"""
	DOCSTRING:

	"""
	def __init__(self):
		server = 'localhost'
		port = 5555

		print(f'[ > ] Binding {server}:{port}')

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.bind((server, port))
		except socket.error as e:
			str(e)

		s.listen()
		print('[ > ] Server started, waiting for connection...')

		self.games = {}
		self.id_count = 0
		self.last_data = -1
		self.waiting = []

		while True:
			conn, addr = s.accept()
			print(f'[ + ] Connected to: {addr}')
			self.id_count += 1

			start_new_thread(self.threaded_clinet, (conn, ))

	def threaded_clinet(self, conn):
		conn.send(str.encode('CONNECTED'))
		p = None
		game_id = None
		while True:
			try:
				data = conn.recv(4096).decode()

				if not data:
					break
				else:
					data_list = data.split()
					if data_list[0] == 'create':
						name = data_list[1]
						size = int(data_list[2])
						pw = data_list[3]
						game_id = len(self.games)
						p = 0
						self.games[game_id] = Game(game_id, name, size, pw)

						self.waiting.append(self.games[game_id])
						print(f'[ + ] Creating a new game... (of size {data_list[2]})')
						
						conn.sendall(pickle.dumps(self.games[game_id]))

					elif data_list[0] == 'get_lobby':
						conn.sendall(pickle.dumps(self.waiting))

					elif data_list[0] == 'join':
						game_id = int(data_list[1])
						self.games[game_id].joined += 1
						p = self.games[game_id].joined - 1

						if self.games[game_id].joined == self.games[game_id].lobby_size:
							self.games[game_id].ready = True
							self.waiting.remove(self.games[game_id])
							print(f'[ + ] Starting a new game... (of size {self.games[game_id].lobby_size})')

						conn.sendall(pickle.dumps(self.games[game_id]))

					elif data_list[0] == 'get':
						game_id = int(data_list[1])

						conn.sendall(pickle.dumps(self.games[game_id]))

					elif data_list[0] == 'get_player':
						conn.sendall(pickle.dumps(p))

					elif data_list[0] == 'quit':
						game.quit = True

						conn.sendall(pickle.dumps(self.games[game_id]))

			except:
				break

		print('[ - ] Lost connection')
		try:
			if game_id in self.games:
				game = self.games[game_id]

				# Check if game in lobby phase
				for size in range(2, 4):
					if game_id in self.waiting[size]:
						self.waiting[size].remove(game_id)

				del self.games[game_id]
				print(f'[ - ] Closing game.. (ID: {game_id})')
		except:
			pass

		self.id_count -= 1
		conn.close()


if __name__ == '__main__':
	Server()