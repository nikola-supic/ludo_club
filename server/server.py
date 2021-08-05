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
					print('[ - ] Lost connection...')
					break
				else:
					data_list = data.split()
					if data_list[0] == 'create':
						print('debug v1')
						name = data_list[1]
						size = int(data_list[2])
						pw = data_list[3]
						price = int(data_list[4])
						game_id = len(self.games)
						p = 0
						self.games[game_id] = Game(game_id, name, size, pw, price)

						self.waiting.append(self.games[game_id])
						print(f'[ + ] Creating a new game... (of size {size})')
						print('debug v2')

						conn.sendall(pickle.dumps(self.games[game_id]))
						print('debug v3')

					elif data_list[0] == 'get_lobby':
						conn.sendall(pickle.dumps(self.waiting))

					elif data_list[0] == 'join':
						game_id = int(data_list[1])
						game = self.games[game_id]

						game.joined += 1
						p = game.joined - 1

						if game.joined == game.lobby_size:
							game.all_connected = True
							game.start()

							self.waiting.remove(game)
							print(f'[ + ] Starting a new game... (of size {game.lobby_size})')

						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'get':
						game = self.games[game_id]
						game_id = int(data_list[1])

						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'get_player':
						conn.sendall(pickle.dumps(p))

					elif data_list[0] == 'username':
						game = self.games[game_id]

						player = int(data_list[1])
						user_name = data_list[2]
						user_id = int(data_list[3])
						avatar = int(data_list[4])

						game.update_users(player, user_name, user_id, avatar)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'dice':
						game = self.games[game_id]
						dice = int(data_list[1])
						dice_skin = int(data_list[2])

						game.rolled_dice = True
						game.dice = dice
						game.dice_skin = dice_skin
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'move':
						game = self.games[game_id]
						player = int(data_list[1])
						pawn_idx = int(data_list[2])
						
						game.rolled_dice = False
						game.move_pawn(player, pawn_idx)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'next_move':
						game = self.games[game_id]
						player = int(data_list[1])
						
						game.rolled_dice = False
						game.player_on_move = game.get_next()

						if game.pawns_finish[player] == 4:
							game.ready = False
							game.give_win(player)
							game.winner = game.user_names[player]

						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'check_eat':
						game = self.games[game_id]

						player = int(data_list[1])
						move_idx = int(data_list[2])

						game.check_eat(player, move_idx)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'msg':
						game = self.games[game_id]
						username = data_list[1]
						msg = ' '.join(data_list[2:])

						game.send_msg(username, msg)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'emoji':
						game = self.games[game_id]

						player = int(data_list[1])
						emoji_idx = int(data_list[2])

						game.send_emoji(player, emoji_idx)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'clear_emoji':
						game = self.games[game_id]

						game.send_emoji(None, None)
						conn.sendall(pickle.dumps(game))

					elif data_list[0] == 'quit':
						game = self.games[game_id]

						game.quit = True
						game.players_left += 1

						conn.sendall(pickle.dumps(game))
						
						if game.players_left == game.joined:
							# Save message history
							if len(game.messages) > 8:
								time = datetime.now()
								time_str = f'{time.day:02d}_{time.month:02d}_{time.year} {time.hour:02d}_{time.minute:02d}_{time.second:02d}'
								filename = f'chat_history/chat_{time_str}.txt'
								with open(filename, 'w') as file:
									game.messages.reverse()
									for msg in game.messages:
										file.write(f'# {msg[2]} // Player {msg[0]} // {msg[1]}\n')

							# Check if game in lobby phase
							if game in self.waiting:
								self.waiting.remove(self.games[game_id])

							del self.games[game_id]
							print(f'[ - ] Closing game.. (ID: {game_id})')

					elif data_list[0] == 'ready':
						game = self.games[game_id]
						game.players_ready += 1

						if game.players_ready == game.lobby_size:
							game.start()

						conn.sendall(pickle.dumps(game))

			except Exception as e:
				print(e)
				print('[ - ] Lost connection... (Error)')
				break

		self.id_count -= 1
		conn.close()


if __name__ == '__main__':
	Server()