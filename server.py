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

		self.waiting = [[] for _ in range(4)]
		
		while True:
			conn, addr = s.accept()
			print(f'[ + ] Connected to: {addr}')
			self.id_count += 1

			lobby_size = int(conn.recv(4096).decode())

			p = None
			for size in range(2, 4):
				if lobby_size == size:
					if len(self.waiting[size]) == 0:
						game_id = len(self.games)
						self.waiting[size].append(game_id)

						p = 0
						self.games[game_id] = Game(game_id, lobby_size)
						print(f'[ + ] Creating a new game... (of size {size})')
						break
					else:
						game_id = self.waiting[size][0]
						self.games[game_id].joined += 1
						p = self.games[game_id].joined - 1

						if self.games[game_id].joined == lobby_size:
							self.games[game_id].ready = True
							self.games[game_id].give_cards()
							self.waiting[size].pop(0)

							print(f'[ + ] Starting a new game... (of size {size})')


			start_new_thread(self.threaded_clinet, (conn, p, game_id))

	def threaded_clinet(self, conn, p, game_id):
		conn.send(str.encode(str(p)))

		while True:
			try:
				data = conn.recv(4096).decode()

				if game_id in self.games:
					game = self.games[game_id]

					if not data:
						break
					else:
						# commands
						pass
				else:
					break
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