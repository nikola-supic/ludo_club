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
from positions import BOARD_POS

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
		self.pawn = []
		self.pawns_finish = [0 for _ in range(lobby_size)]
		self.pawns_free = [0 for _ in range(lobby_size)]
		self.player_on_move = None
		self.rolled_dice = False
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


	def start_from_color(self, player):
		pos = {
			0 : 1,
			1 : 27,
			2 : 40,
			3 : 14
		}
		return pos[player]


	def last_from_color(self, player):
		pos = {
			0 : 51,
			1 : 25,
			2 : 38,
			3 : 12
		}
		return pos[player]


	def move_pawn(self, player, move_idx):
		for player_idx, color in enumerate(self.pawn):
			if player_idx == player:
				for pawn_idx, pawn in enumerate(color):
					if pawn_idx == move_idx:
						if pawn.finish:
							if pawn.pos+1 == 5:
								del self.pawn[player_idx][pawn_idx]
								self.pawns_finish[player] += 1
								self.pawns_free[player] -= 1
								break
							else:
								pawn.pos += 1
						else:
							if pawn.pos < 0:
								pawn.pos = self.start_from_color(player_idx)
								self.pawns_free[player] += 1
							else:
								if pawn.pos == self.last_from_color(player_idx):
									pawn.pos = 0
									pawn.finish = True
								else:
									if pawn.pos+1 == len(BOARD_POS):
										pawn.pos = 0
									else:
										pawn.pos += 1

	def get_next(self):
		next_player = None
		if self.player_on_move == self.lobby_size-1:
			next_player = 0
		else:
			next_player = self.player_on_move + 1
		return next_player 


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
		self.finish = False
		self.button = None
		
	def __str__(self):
		return f'{self.color}-{self.pos}-{self.img}'
		
	def __repr__(self):
		return f'{self.color}-{self.pos}-{self.img}'