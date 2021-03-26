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
					print('[ - ] DATA BREAK')
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
							self.games[game_id].time_started = datetime.now()
							self.waiting.remove(self.games[game_id])
							print(f'[ + ] Starting a new game... (of size {self.games[game_id].lobby_size})')

						conn.sendall(pickle.dumps(self.games[game_id]))

					elif data_list[0] == 'get':
						game_id = int(data_list[1])

						conn.sendall(pickle.dumps(self.games[game_id]))

					elif data_list[0] == 'get_player':
						conn.sendall(pickle.dumps(p))

					elif data_list[0] == 'quit':
						self.games[game_id].quit = True
						self.games[game_id].players_left += 1

						conn.sendall(pickle.dumps(self.games[game_id]))
						
						if self.games[game_id].players_left == self.games[game_id].joined:
							# Check if game in lobby phase
							if self.games[game_id] in self.waiting:
								self.waiting.remove(self.games[game_id])

							del self.games[game_id]
							print(f'[ - ] Closing game.. (ID: {game_id})')


			except:
				print('[ - ] ERROR BREAK')
				break

		print('[ - ] Lost connection')
		self.id_count -= 1
		conn.close()


if __name__ == '__main__':
	Server()