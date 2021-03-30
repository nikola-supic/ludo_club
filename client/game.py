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
	def __init__(self, id, lobby_name, lobby_size, lobby_pw, lobby_price):
		self.id = id
		self.lobby_name = lobby_name
		self.lobby_size = lobby_size
		self.lobby_pw = lobby_pw
		self.lobby_price = lobby_price
		self.joined = 1
		self.all_connected = False
		self.quit = False
		self.players_left = 0

		self.ready = False
		self.players_ready = 0
		self.time_started = 0
		self.winner = None
		self.pawn = []
		self.pawns_finish = [0 for _ in range(lobby_size)]
		self.pawns_free = [0 for _ in range(lobby_size)]
		self.player_on_move = None
		self.rolled_dice = False
		self.dice = 1
		self.dice_skin = 1
		self.give_exp = False
		self.give_finish_exp = False

		self.user_names = ['' for _ in range(lobby_size)]
		self.user_ids = [0 for _ in range(lobby_size)]
		self.user_avatars = [0 for _ in range(lobby_size)]
		self.wins = [0 for _ in range(lobby_size)]
		self.defeats = [0 for _ in range(lobby_size)]
		self.lobby_started = datetime.now()
		self.messages = []
		self.emoji = None
		self.emoji_player = None


	def start(self):
		self.reset()
		for idx, color in enumerate(['green', 'blue', 'yellow', 'red']):
			self.pawn.append([])
			for i in range(1, 5):
				self.pawn[idx].append( Pawn(color, i*-1, f'images/pawn/{color}.png') )

			if idx == self.lobby_size-1:
				break

		self.player_on_move = randint(0, self.lobby_size-1)


	def reset(self):
		self.ready = True
		self.players_ready = 0
		self.time_started = datetime.now()
		self.winner = None
		self.pawn = []
		self.pawns_finish = [0 for _ in range(self.lobby_size)]
		self.pawns_free = [0 for _ in range(self.lobby_size)]
		self.player_on_move = None
		self.rolled_dice = False
		self.dice = 1


	def connected(self):
		return self.all_connected


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
		self.give_exp = False
		self.give_finish_exp = False
		for player_idx, color in enumerate(self.pawn):
			if player_idx == player:
				for pawn_idx, pawn in enumerate(color):
					if pawn_idx == move_idx:
						if pawn.finish:
							if pawn.pos+1 == 5:
								del self.pawn[player_idx][pawn_idx]
								self.pawns_finish[player] += 1
								self.pawns_free[player] -= 1
								self.give_finish_exp = True
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
									if pawn.pos+1 == 52:
										pawn.pos = 0
									else:
										pawn.pos += 1


	def check_eat(self, player, move_idx):
		for player_idx, color in enumerate(self.pawn):
			if player_idx != player:
				for pawn_idx, pawn in enumerate(color):
					if pawn.pos == self.pawn[player][move_idx].pos:
						if pawn.pos not in [8, 34, 47, 21]:
							self.pawn[player_idx][pawn_idx].pos = (pawn_idx+1) * (-1)
							self.pawns_free[player_idx] -= 1
							self.give_exp = True
							break


	def get_next(self):
		next_player = None
		if self.player_on_move == self.lobby_size-1:
			next_player = 0
		else:
			next_player = self.player_on_move + 1
		return next_player 


	def give_win(self, player):
		self.wins[player] += 1

		for idx in range(self.lobby_size):
			if idx != player:
				self.defeats[idx] += 1


	def update_users(self, player, username, id, avatar):
		self.user_names[player] = username
		self.user_ids[player] = id
		self.user_avatars[player] = avatar


	def send_msg(self, username, message):
		time = datetime.now()
		time_str = f'{time.hour:02d}:{time.minute:02d}:{time.second:02d}'
		self.messages.insert(0, [username, message, time_str])


	def send_emoji(self, player, emoji):
		self.emoji = emoji
		self.emoji_player = player


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