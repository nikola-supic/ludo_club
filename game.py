"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: game.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3
from datetime import datetime

class Game():
	def __init__(self, id, lobby_name, lobby_size, lobby_pw):
		self.id = id
		self.lobby_name = lobby_name
		self.lobby_size = lobby_size
		self.lobby_pw = lobby_pw
		self.joined = 1
		self.ready = False
		self.quit = False
		self.winner = None
		self.player_on_move = None
		self.time_started = 0

		self.user_names = ['' for _ in range(lobby_size)]
		self.user_ids = [0 for _ in range(lobby_size)]
		self.wins = [0 for _ in range(lobby_size)]
		self.lobby_started = datetime.now()
		self.messages = []

	def reset(self):
		self.winner = None
		self.player_on_move = None
		self.time_started = 0

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

	def get_defeats(self, player):
		defeats = 0
		for idx, wins in enumerate(self.wins):
			if player != idx:
				defeats += wins
		return defeats

	def update_users(self, player, username, id):
		self.user_names[player] = username
		self.user_ids[player] = id

	def send_msg(self, username, message):
		time = datetime.now()
		time_str = f'{time.hour:02d}:{time.minute:02d}:{time.second:02d}'
		self.messages.insert(0, [username, message, time_str])