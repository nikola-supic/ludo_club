"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: game.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3
from datetime import datetime
from random import randint

class Game():
	def __init__(self, id, lobby_name, lobby_size, lobby_pw):
		self.id = id
		self.lobby_name = lobby_name
		self.lobby_size = lobby_size
		self.lobby_pw = lobby_pw
		self.joined = 1
		self.ready = False
		self.quit = False
		self.players_left = 0

		self.time_started = 0
		self.winner = None
		self.player_on_move = None
		self.dice = 1

		self.user_names = ['' for _ in range(lobby_size)]
		self.user_ids = [0 for _ in range(lobby_size)]
		self.wins = [0 for _ in range(lobby_size)]
		self.defeats = [0 for _ in range(lobby_size)]
		self.lobby_started = datetime.now()
		self.messages = []

	def start(self):
		self.pawn = []
		for idx, color in enumerate(['green', 'blue', 'yellow', 'red']):
			self.pawn.append([])
			for i in range(1, 5):
				self.pawn[idx].append( Pawn(color, i*-1, f'images/pawn/{color}.png') )

			if idx == self.lobby_size-1:
				break

		self.player_on_move = randint(0, self.lobby_size-1)


	def reset(self):
		self.time_started = 0
		self.winner = None
		self.player_on_move = None

	def connected(self):
		return self.ready

	def player_left(self):
		return self.quit

	def get_player_move(self):
		return self.player_on_move

	def check_is_winner(self, player):
		pass

	def give_win(self, player):
		self.wins[player] += 1

	def update_users(self, player, username, id):
		self.user_names[player] = username
		self.user_ids[player] = id

	def send_msg(self, username, message):
		time = datetime.now()
		time_str = f'{time.hour:02d}:{time.minute:02d}:{time.second:02d}'
		self.messages.insert(0, [username, message, time_str])

class Pawn():
	"""
	DOCSTRING:

	"""
	def __init__(self, color, pos, img):
		self.color = color
		self.pos = pos
		self.img = img
		
	def __str__(self):
		return f'{self.color}-{self.pos}-{self.img}'
		
	def __repr__(self):
		return f'{self.color}-{self.pos}-{self.img}'