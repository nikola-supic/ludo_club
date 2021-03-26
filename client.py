"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: client.py
@description: ->
	DOCSTRING:
"""
#!/usr/bin/env python3

import pygame
import pickle
import sys
from datetime import datetime, timedelta
from random import randint
import os

from game import Game
from network import Network
from customs import Text, Button, ImageButton, InputBox
from positions import BOARD_POS
from positions import GREEN_FINISH, RED_FINISH, BLUE_FINISH, YELLOW_FINISH
from positions import GREEN_START, RED_START, BLUE_START, YELLOW_START
import user

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (237, 28, 36)
BLUE = (15, 39, 99)
YELLOW = (255, 214, 7)

CARD_WIDTH = 80
CARD_HEIGHT = 140

DECK_WIDTH = 60
DECK_HEIGHT = 100

pygame.font.init()
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

def get_music():
	songs_list = []
	os.chdir('music')
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	for mp3 in files:
		if mp3.endswith('.mp3'):
			songs_list.append(mp3)

	os.chdir('..')
	return songs_list

class App():
	"""
	DOCSTRING:

	"""
	def __init__(self, width, height):
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width, height))
		icon = pygame.image.load("images/logo.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption('Ludo Club')

		self.user = None
		self.show_info = False
		self.network = None
		self.player = None


	def background_music(self):
		songs_list = get_music()
		rand = randint(0, len(songs_list)-1)

		pygame.mixer.music.load('music//' + songs_list[rand])
		pygame.mixer.music.set_volume(self.user.volume / 100)
		pygame.mixer.music.play()


	def draw_error(self, msg):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/game_error.png")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, f'{msg}', (self.width/2, self.height-60), WHITE, text_size=40, center=True)
		pygame.display.update()


	def welcome(self):
		pygame.display.set_caption('Ludo Club (Welcome)')
		click = False

		# Create left part of screen
		login_name = InputBox(self.screen, (self.width/2-120, self.height - 150), (240, 30), 'Sule', BLUE, WHITE)
		login_pass = InputBox(self.screen, (self.width/2-120, self.height - 100), (240, 30), '12345678', BLUE, WHITE)
		login_button = Button(self.screen, 'LOGIN', (self.width/2-120, self.height - 60), (240, 40), BLUE, text_color=WHITE, border=2, border_color=WHITE)

		# Create right part of screen
		register_name = InputBox(self.screen, (self.width/2-120, 80), (240, 30), '', BLUE, WHITE)
		register_mail = InputBox(self.screen, (self.width/2-120, 130), (240, 30), '', BLUE, WHITE)
		register_pass = InputBox(self.screen, (self.width/2-120, 180), (240, 30), '', BLUE, WHITE)
		register_button = Button(self.screen, 'REGISTER', (self.width/2-120, 220), (240, 40), BLUE, text_color=WHITE, border=2, border_color=WHITE)

		while True:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/welcome.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'LUDO CLUB', (self.width/2, 30), WHITE, text_size=44, center=True)
			Text(self.screen, 'PLEASE ENTER YOUR INFORMATION', (self.width/2, 50), BLUE, text_size=20, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			# Draw bottom part of screen
			Text(self.screen, 'ENTER USERNAME:', (self.width/2-120, self.height-160), WHITE, text_size=18)
			login_name.draw()
			Text(self.screen, 'ENTER PASSWORD:', (self.width/2-120, self.height-110), WHITE, text_size=18)
			login_pass.draw()
			login_button.draw()

			# Draw top part of screen
			Text(self.screen, 'ENTER USERNAME:', (self.width/2-120, 70), WHITE, text_size=18)
			register_name.draw()
			Text(self.screen, 'ENTER E-MAIL:', (self.width/2-120, 120), WHITE, text_size=18)
			register_mail.draw()
			Text(self.screen, 'ENTER PASSWORD:', (self.width/2-120, 170), WHITE, text_size=18)
			register_pass.draw()
			register_button.draw()

			mx, my = pygame.mouse.get_pos()
			if login_button.rect.collidepoint((mx, my)):
				if click:
					self.user = user.check_login(login_name.text, login_pass.text)
					if self.user != None:
						self.main_menu()
					else:
						Text(self.screen, 'WRONG USERNAME OR PASSWORD.', (self.width/2,  self.height-180), BLUE, text_size=28, center=True)
						login_name.clear()
						login_pass.clear()

						pygame.display.update()
						pygame.time.delay(1500)

			if register_button.rect.collidepoint((mx, my)):
				if click:
					register_name.text.replace(' ', '_')

					if user.check_register(register_name.text, register_mail.text, register_pass.text):
						register_name.clear()
						register_mail.clear()
						register_pass.clear()
						
						Text(self.screen, 'SUCCESSFULY REGISTERED, USE THAT INFO TO LOGIN.', (self.width/2, self.height-180), BLUE, text_size=28, center=True)
						pygame.display.update()
						pygame.time.delay(1500)
					else:
						register_name.clear()
						register_mail.clear()
						register_pass.clear()
						
						Text(self.screen, 'YOU ENTERED SOME WRONG INFO. TRY AGAIN.', (self.width/2, self.height-180), BLUE, text_size=28, center=True)
						pygame.display.update()
						pygame.time.delay(1500)


			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				login_name.handle_event(event)
				login_pass.handle_event(event)
				register_name.handle_event(event)
				register_mail.handle_event(event)
				register_pass.handle_event(event)

			login_name.update()
			login_pass.update()
			register_name.update()
			register_mail.update()
			register_pass.update()

			pygame.display.update()
			clock.tick(60)


	def main_menu(self):
		self.background_music()
		self.network = Network()

		click = False

		button_settings = ImageButton(self.screen, 'images/main_settings.png', (120, 120), (70, self.height/2 - 70), 'settings')
		button_lobby = ImageButton(self.screen, 'images/main_start_grey.png', (160, 160), (self.width/2 - 80, self.height/2 - 120), 'start')
		button_create = ImageButton(self.screen, 'images/main_start_red.png', (160, 160), (self.width/2 - 80, self.height/2 + 10), 'start')
		button_admin = ImageButton(self.screen, 'images/main_admin.png', (120, 120), (self.width - 200, self.height/2 - 70), 'exit')

		while True:
			pygame.display.set_caption('Ludo Club (Main Menu)')

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'LUDO CLUB', (self.width/2, 100), BLUE, text_size=72, center=True)
			Text(self.screen, 'MAIN MENU', (self.width/2, 130), WHITE, text_size=24, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			button_settings.draw()
			Text(self.screen, 'SETTINGS', (70 + 60, self.height/2 + 60), WHITE, text_size=24, center=True)
			button_lobby.draw()
			Text(self.screen, 'PICK LOBBY', (self.width/2, self.height/2 - 105), WHITE, text_size=24, center=True)
			button_create.draw()
			Text(self.screen, 'NEW LOBBY', (self.width/2, self.height/2 + 155), WHITE, text_size=24, center=True)
			button_admin.draw()
			Text(self.screen, 'ADMIN PANEL', (self.width - 210 + 70, self.height/2 + 60), WHITE, text_size=24, center=True)

			mx, my = pygame.mouse.get_pos()
			if click:
				if button_lobby.click((mx, my)):
					self.pick_lobby()

				elif button_create.click((mx, my)):
					self.create_lobby()

				elif button_settings.click((mx, my)):	
					self.settings()

				elif button_admin.click((mx, my)):
					if self.user.admin:
						self.admin_panel()
					else:
						self.draw_error('You do not have admin permissions.')
						pygame.time.delay(1000)

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.user.user_quit()
						pygame.quit()
						sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				if event.type == MUSIC_END:
					self.background_music()

			pygame.display.update()
			clock.tick(60)


	def settings(self):
		pygame.display.set_caption('Ludo Club (Settings)')
		run = True
		click = False
		
		username = InputBox(self.screen, (self.width/2 - 150, 190), (300, 30), '', BLUE, WHITE)
		email = InputBox(self.screen, (self.width/2 - 150, 240), (300, 30), '', BLUE, WHITE)
		password = InputBox(self.screen, (self.width/2 - 150, 290), (300, 30), '', BLUE, WHITE)
		volume = InputBox(self.screen, (self.width/2 - 150, 340), (300, 30), '', BLUE, WHITE)
		save = Button(self.screen, 'SAVE INFO', (self.width/2 - 150, self.height-50), (300, 30), BLUE, text_color=WHITE, border=2, border_color=WHITE)
		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'LUDO CLUB', (self.width/2, 100), BLUE, text_size=72, center=True)
			Text(self.screen, 'SETTINGS', (self.width/2, 130), WHITE, text_size=24, center=True)
			Text(self.screen, 'TO CHANGE INFO, ENTER NEW INFO AND PRESS SAVE', (self.width/2, 145), BLUE, text_size=20, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			Text(self.screen, f'Current username: {self.user.username}', (self.width/2, 180), WHITE, text_size=18, center=True)
			username.draw()
			Text(self.screen, f'Current e-mail: {self.user.email}', (self.width/2, 230), WHITE, text_size=18, center=True)
			email.draw()
			Text(self.screen, f'Current password: {self.user.password}', (self.width/2, 280), WHITE, text_size=18, center=True)
			password.draw()
			Text(self.screen, f'Current volume: {self.user.volume}', (self.width/2, 330), WHITE, text_size=18, center=True)
			volume.draw()

			Text(self.screen, f'Your wins: {self.user.wins}', (self.width/2, self.height-90), WHITE, text_size=18, center=True)
			Text(self.screen, f'Your defeats: {self.user.defeats}', (self.width/2, self.height-75), WHITE, text_size=18, center=True)
			Text(self.screen, f'REGISTRATION DATE: {self.user.register_date}', (self.width/2, self.height-60), WHITE, text_size=18, center=True)

			save.draw()
			exit_btn.draw()

			mx, my = pygame.mouse.get_pos()
			if click:
				if save.rect.collidepoint((mx, my)):
					if username.text != '':
						username.text.replace(' ', '_')
						self.user.change_username(username.text)
						username.clear()

					if email.text != '':
						self.user.change_email(email.text)
						email.clear()

					if password.text != '':
						self.user.change_password(password.text)
						password.clear()

					if volume.text != '':
						value = int(volume.text)
						if value < 0 or value > 100:
							self.draw_error('Volume value must be between 0 and 100.')
							pygame.time.delay(1000)
						else:
							self.user.change_volume(value)
							pygame.mixer.music.set_volume(value / 100)
						
						volume.clear()

				if exit_btn.click((mx, my)):
					run = False

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				username.handle_event(event)
				email.handle_event(event)
				password.handle_event(event)
				volume.handle_event(event)

			username.update()
			email.update()
			password.update()
			volume.update()

			pygame.display.update()
			clock.tick(60)


	def admin_panel(self):
		pygame.display.set_caption('Ludo Club (Admin Panel)')
		run = True
		click = False
		see_online = False

		admin_permission = InputBox(self.screen, (self.width/2 - 150, 190), (300, 30), '', BLUE, WHITE)
		ban_player = InputBox(self.screen, (self.width/2 - 150, 240), (300, 30), '', BLUE, WHITE)
		reset_stats = InputBox(self.screen, (self.width/2 - 150, 290), (300, 30), '', BLUE, WHITE)
		see_pw = InputBox(self.screen, (self.width/2 - 150, 340), (300, 30), '', BLUE, WHITE)
		last_online = InputBox(self.screen, (self.width/2 - 150, 390), (300, 30), '', BLUE, WHITE)
		
		online_players = Button(self.screen, 'SEE ONLINE PLAYERS', (self.width/2 - 150, self.height-90), (300, 30), BLUE, text_color=WHITE, border=2, border_color=WHITE)
		refresh = Button(self.screen, 'REFRESH', (self.width/2 - 150, self.height-50), (300, 30), BLUE, text_color=WHITE, border=2, border_color=WHITE)
		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'LUDO CLUB', (self.width/2, 100), BLUE, text_size=72, center=True)
			Text(self.screen, 'ADMIN PANEL', (self.width/2, 130), WHITE, text_size=24, center=True)
			Text(self.screen, 'PLEASE BE CAREFUL WHILE USING THIS ADMIN PANEL', (self.width/2, 145), BLUE, text_size=20, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			Text(self.screen, 'Give admin permissions: (User ID)', (self.width/2, 180), WHITE, text_size=18, center=True)
			admin_permission.draw()
			Text(self.screen, 'Ban user from game: (User ID)', (self.width/2, 230), WHITE, text_size=18, center=True)
			ban_player.draw()
			Text(self.screen, 'Reset wins & defeats: (User ID)', (self.width/2, 280), WHITE, text_size=18, center=True)
			reset_stats.draw()
			Text(self.screen, 'See password: (User ID)', (self.width/2, 330), WHITE, text_size=18, center=True)
			see_pw.draw()
			Text(self.screen, 'Last online: (User ID)', (self.width/2, 380), WHITE, text_size=18, center=True)
			last_online.draw()

			online_players.draw()
			refresh.draw()
			exit_btn.draw()

			if see_online:
				result = user.online_players()
				y = 180
				for row in result:
					Text(self.screen, f'#{row[0]} // {row[1]}', (20, y), WHITE, text_size=16)
					y += 15

			mx, my = pygame.mouse.get_pos()
			if click:
				if refresh.rect.collidepoint((mx, my)):
					if admin_permission.text != '':
						user.admin_permission(admin_permission.text)

						admin_permission.clear()
						pygame.display.update()

					if ban_player.text != '':
						user.ban_player(ban_player.text)

						ban_player.clear()
						pygame.display.update()

					if reset_stats.text != '':
						user.reset_stats(reset_stats.text)

						reset_stats.clear()
						pygame.display.update()

					if see_pw.text != '':
						user_id = see_pw.text
						pw = user.see_pw(see_pw.text)
						see_pw.clear()

						Text(self.screen, f'User ID: {user_id} // PW: {pw}', (self.width/2, self.height-100), WHITE, text_size=20, center=True)
						pygame.display.update()
						pygame.time.delay(2000)

					if last_online.text != '':
						user_id = last_online.text
						online = user.last_online(last_online.text)
						last_online.clear()

						Text(self.screen, f'User ID: {user_id} // Last Online: {online}', (self.width/2, self.height-115), WHITE, text_size=20, center=True)
						pygame.display.update()
						pygame.time.delay(2000)

				if online_players.rect.collidepoint((mx, my)):
					if see_online:
						see_online = False
					else:
						see_online = True

				if exit_btn.click((mx, my)):
					run = False

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				admin_permission.handle_event(event)
				ban_player.handle_event(event)
				reset_stats.handle_event(event)
				see_pw.handle_event(event)
				last_online.handle_event(event)

			admin_permission.update()
			ban_player.update()
			reset_stats.update()
			see_pw.update()
			last_online.update()

			pygame.display.update()
			clock.tick(60)


	def create_lobby(self):
		pygame.display.set_caption('Ludo Club (Admin Panel)')
		run = True
		click = False

		lobby_name = InputBox(self.screen, (self.width/2 - 150, 190), (300, 30), 'lobby', BLUE, WHITE)
		lobby_size = InputBox(self.screen, (self.width/2 - 150, 240), (300, 30), '2', BLUE, WHITE)
		lobby_pw = InputBox(self.screen, (self.width/2 - 150, 290), (300, 30), '', BLUE, WHITE)

		create = Button(self.screen, 'CREATE', (self.width/2 - 150, self.height-50), (300, 30), BLUE, text_color=WHITE, border=2, border_color=WHITE)
		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))
			Text(self.screen, 'LUDO CLUB', (self.width/2, 100), BLUE, text_size=72, center=True)
			Text(self.screen, 'CREATING NEW LOBBY', (self.width/2, 130), WHITE, text_size=24, center=True)
			Text(self.screen, 'ENTER INFORMATION ABOUT LOBBY YOU WANT TO CREATE', (self.width/2, 145), BLUE, text_size=20, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			Text(self.screen, 'Enter lobby name:', (self.width/2, 180), WHITE, text_size=18, center=True)
			lobby_name.draw()
			Text(self.screen, 'Enter lobby size:', (self.width/2, 230), WHITE, text_size=18, center=True)
			lobby_size.draw()
			Text(self.screen, 'Enter lobby password:', (self.width/2, 280), WHITE, text_size=18, center=True)
			lobby_pw.draw()

			create.draw()
			exit_btn.draw()

			mx, my = pygame.mouse.get_pos()
			if click:
				if create.rect.collidepoint((mx, my)):
					try:
						size = int(lobby_size.text)

						if lobby_name.text == '' or len(lobby_name.text) > 24:
							self.draw_error('You need to enter valid name for lobby.')
							pygame.time.delay(1500)
						
						elif size < 2 or size > 4:
							self.draw_error('You need to enter number between 2 and 4.')
							pygame.time.delay(1500)
						
						else:
							lobby_name.text.replace(' ', '_')
							if lobby_pw.text == '':
								pw = None
							else:
								lobby_pw.text.replace(' ', '_')
								pw = lobby_pw.text

							try:
								run = False
								game = self.network.send(f'create {lobby_name.text} {size} {pw}')
								self.game_screen(game.id)
							except:
								self.draw_error('Game error #404.')
								pygame.time.delay(1500)
								run = False

					except ValueError:
						self.draw_error('You need to enter number between 2 and 4.')
						pygame.time.delay(1500)
						run = False

				if exit_btn.click((mx, my)):
					run = False

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				lobby_name.handle_event(event)
				lobby_size.handle_event(event)
				lobby_pw.handle_event(event)

			lobby_name.update()
			lobby_size.update()
			lobby_pw.update()

			pygame.display.update()
			clock.tick(60)


	def draw_lobby(self, idx, game):
		row = idx // 2
		col = idx % 2
		x = 90 + col * 270
		y = 50 + row * 160

		join_btn = Button(self.screen, 'JOIN', (x+131, y+100), (105, 28), BLUE, text_color=WHITE)
		join_btn.draw()

		lobby_bg = pygame.image.load("images/lobby.png")
		lobby_bg = pygame.transform.scale(lobby_bg, (250, 140))
		self.screen.blit(lobby_bg, (x, y))

		Text(self.screen, f'ID #{idx}', (x+60, y+13), WHITE, text_size=20)
		Text(self.screen, f'NAME: {game.lobby_name}', (x+18, y+40), RED, text_size=20)
		Text(self.screen, f'JOINED: {game.joined} / {game.lobby_size}', (x+18, y+60), RED, text_size=20)

		if game.lobby_pw != 'None':
			locked = pygame.image.load("images/locked.png")
			locked = pygame.transform.scale(locked, (32, 32))
			self.screen.blit(locked, (x+210, y+30))

		else:
			unlocked = pygame.image.load("images/unlocked.png")
			unlocked = pygame.transform.scale(unlocked, (32, 32))
			self.screen.blit(unlocked, (x+210, y+30))

		return join_btn


	def pick_lobby(self):
		pygame.display.set_caption('Ludo Club (Pick lobby)')
		run = True
		click = False

		input_pw = InputBox(self.screen, (90, self.height-45), (250, 30), '', RED, WHITE)
		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (20, self.height - 45), 'exit')
		while run:
			try:
				waiting = self.network.send('get_lobby')

				if not waiting:
					self.draw_error('There is no games waiting for player.')
					pygame.time.delay(2500)
					run = False
					break
			except:
				self.draw_error('Could not get games.')
				pygame.time.delay(2500)
				run = False
				break

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			join_btn_dict = {}
			for idx, game in enumerate(waiting):
				join_btn = self.draw_lobby(idx, game)
				join_btn_dict[game.id] = join_btn

			input_pw.draw()
			Text(self.screen, 'Enter lobby password:', (90, self.height-55), WHITE, text_size=18)
			exit_btn.draw()
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			mx, my = pygame.mouse.get_pos()
			if click:
				if exit_btn.click((mx, my)):
					run = False

				for idx, game in enumerate(waiting):
					if join_btn_dict[game.id].rect.collidepoint((mx, my)):
						if game.lobby_pw == 'None':
							game = self.network.send(f'join {game.id}')
							run = False

							self.game_screen(game.id)
						else:
							if game.lobby_pw == input_pw.text:
								game = self.network.send(f'join {game.id}')
								run = False

								self.game_screen(game.id)
							else:
								self.draw_error('Wrong password.')
								pygame.time.delay(2500)


			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				input_pw.handle_event(event)
			input_pw.update()

			pygame.display.update()
			clock.tick(60)
		

	def draw_waiting(self, game):
		duration = int((datetime.now() - game.lobby_started).total_seconds())
		x = self.width/2 - 190
		y = self.height/2 - 100

		self.screen.fill(BLACK)
		bg = pygame.image.load("images/background.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))

		window = pygame.image.load("images/lobby.png")
		window = pygame.transform.scale(window, (380, 200))
		self.screen.blit(window, (x, y))

		Text(self.screen, 'Waiting for players to join...', (x+90, y+19), WHITE, text_size=20)
		Text(self.screen, f'WAITING TIME: {timedelta(seconds=duration)}', (x+25, y+50), RED, text_size=24)
		Text(self.screen, f'JOINED: {game.joined} / {game.lobby_size}', (x+25, y+70), RED, text_size=24)
		Text(self.screen, f'PASSWORD: {game.lobby_pw}', (x+25, y+90), RED, text_size=24)
		Button(self.screen, 'WAITING...', (x+210, y+144), (140, 39), RED, text_size=30, text_color=WHITE).draw()
		Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

		pygame.display.update()


	def draw_quitting(self, game):
		pygame.display.set_caption('Ludo Club (Player Left)')

		run = True
		click = False
		duration = int((datetime.now() - game.time_started).total_seconds())
		while run:
			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			x = self.width/2 - 190
			y = self.height/2 - 100

			window = pygame.image.load("images/lobby.png")
			window = pygame.transform.scale(window, (380, 200))
			self.screen.blit(window, (x, y))

			Text(self.screen, 'One of the player left', (x+90, y+19), WHITE, text_size=20)
			Text(self.screen, f'GAME TIME: {timedelta(seconds=duration)}', (x+25, y+50), RED, text_size=24)
			Text(self.screen, f'WINS: {game.wins[self.player]}', (x+25, y+70), RED, text_size=24)
			Text(self.screen, f'DEFEATS: {game.defeats[self.player]}', (x+25, y+90), RED, text_size=24)
			Button(self.screen, 'QUIT...', (x+210, y+144), (140, 39), RED, text_size=30, text_color=WHITE).draw()
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			mx, my = pygame.mouse.get_pos()
			if click:
				pass

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game = self.network.send(f'quit')
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						game = self.network.send(f'quit')
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

			pygame.display.update()
			clock.tick(60)


	def draw_winner(self, game):
		duration = int((datetime.now() - game.time_started).total_seconds())
		x = self.width/2 - 190
		y = 25

		self.screen.fill(BLACK)
		bg = pygame.image.load("images/game_winner.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))

		window = pygame.image.load("images/lobby.png")
		window = pygame.transform.scale(window, (380, 200))
		self.screen.blit(window, (x, y))

		Text(self.screen, 'We have a winner!', (x+90, y+19), WHITE, text_size=20)
		Text(self.screen, f'GAME TIME: {timedelta(seconds=duration)}', (x+25, y+50), RED, text_size=24)
		Text(self.screen, f'WINNER: {game.winner}', (x+25, y+70), RED, text_size=24)
		Button(self.screen, 'WINNER...', (x+210, y+144), (140, 39), RED, text_size=30, text_color=WHITE).draw()
		Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

		pygame.display.update()


	def draw_pawns(self, game):
		your_pawns = []
		for player, player_pawn in enumerate(game.pawn):
			for idx, pawn in enumerate(player_pawn):
				if pawn.pos < 0:
					pos = pawn.pos * (-1) - 1
					if pawn.color == 'green':
						x = 50 + GREEN_START[pos][0] + 5
						y = 50 + GREEN_START[pos][1] + 5

					if pawn.color == 'red':
						x = 50 + RED_START[pos][0] + 5
						y = 50 + RED_START[pos][1] + 5

					if pawn.color == 'blue':
						x = 50 + BLUE_START[pos][0] + 5
						y = 50 + BLUE_START[pos][1] + 5

					if pawn.color == 'yellow':
						x = 50 + YELLOW_START[pos][0] + 5
						y = 50 + YELLOW_START[pos][1] + 5

					pawn.button = ImageButton(self.screen, pawn.img, (30, 30), (x, y), 'pawn')
					pawn.button.draw()

				else:
					if pawn.finish:
						if pawn.color == 'green':
							x = 50 + GREEN_FINISH[pawn.pos][0] + 5
							y = 50 + GREEN_FINISH[pawn.pos][1] + 5

						if pawn.color == 'red':
							x = 50 + RED_FINISH[pawn.pos][0] + 5
							y = 50 + RED_FINISH[pawn.pos][1] + 5

						if pawn.color == 'blue':
							x = 50 + BLUE_FINISH[pawn.pos][0] + 5
							y = 50 + BLUE_FINISH[pawn.pos][1] + 5

						if pawn.color == 'yellow':
							x = 50 + YELLOW_FINISH[pawn.pos][0] + 5
							y = 50 + YELLOW_FINISH[pawn.pos][1] + 5

					else:
						x = 50 + BOARD_POS[pawn.pos][0] + 5
						y = 50 + BOARD_POS[pawn.pos][1] + 5

					pawn.button = ImageButton(self.screen, pawn.img, (24, 24), (x, y), 'pawn')
					pawn.button.draw()

				if self.player == player:
					your_pawns.append(pawn)

		return your_pawns

	def draw_dice(self, game):
		if not game.rolled_dice:
			colors = {
				0 : GREEN,
				1 : BLUE,
				2 : YELLOW,
				3 : RED
			}
			color = colors[game.player_on_move]
		else:
			color = WHITE

		rect = pygame.Rect(self.width/2-25, self.height/2-25, 50, 50)
		pygame.draw.rect(self.screen, color, rect)

		dice_button = ImageButton(self.screen, f'images/cube/cube_{game.dice}.png', (40, 40), (self.width/2 - 20, self.height/2 - 20), 'cube')
		dice_button.draw()
		return dice_button

	def draw_players(self, game):
		for idx, user_name in enumerate(game.user_names):
			user_id = game.user_ids[idx]
			wins = game.wins[idx]
			defeats = game.defeats[idx]
			finished = game.pawns_finish[idx]

			if idx == 0:
				x, y = 75, 80
				Text(self.screen, f'{user_name} # {user_id}', (x, y), BLACK, text_size=16)
				Text(self.screen, f'{wins}W / {defeats}D', (x, y+11), BLACK, text_size=16)
				if game.player_on_move == idx:
					Text(self.screen, 'Move', (x, y+22), BLACK, text_size=16)

				Text(self.screen, f'{finished}', (self.width/2-30, self.height/2), BLACK, text_size=16, right=True)

			if idx == 1:
				x, y = 625, 620
				Text(self.screen, f'{user_name} # {user_id}', (x, y-11), BLACK, text_size=16, right=True)
				Text(self.screen, f'{wins}W / {defeats}D', (x, y), BLACK, text_size=16, right=True)
				if game.player_on_move == idx:
					Text(self.screen, 'Move', (x, y-22), BLACK, text_size=16, right=True)

				Text(self.screen, f'{finished}', (self.width/2+30, self.height/2), BLACK, text_size=16)

			if idx == 2:
				x, y = 75, 620
				Text(self.screen, f'{user_name} # {user_id}', (x, y-11), BLACK, text_size=16)
				Text(self.screen, f'{wins}W / {defeats}D', (x, y), BLACK, text_size=16)
				if game.player_on_move == idx:
					Text(self.screen, 'Move', (x, y-22), BLACK, text_size=16)

				Text(self.screen, f'{finished}', (self.width/2, self.height/2+30), BLACK, text_size=16, center=True)

			if idx == 3:
				x, y = 625, 80
				Text(self.screen, f'{user_name} # {user_id}', (x, y), BLACK, text_size=16, right=True)
				Text(self.screen, f'{wins}W / {defeats}D', (x, y+11), BLACK, text_size=16, right=True)
				if game.player_on_move == idx:
					Text(self.screen, 'Move', (x, y+22), BLACK, text_size=16, right=True)

				Text(self.screen, f'{finished}', (self.width/2, self.height/-30), BLACK, text_size=16, center=True)

	def draw_game_screen(self, game):
		game_duration = int((datetime.now() - game.time_started).total_seconds())
		lobby_duration = int((datetime.now() - game.lobby_started).total_seconds())

		Text(self.screen, f'Your color: {self.color_from_player()}', (70, 18), WHITE)
		Text(self.screen, f'Game duration: {timedelta(seconds=game_duration)}', (70, 36), WHITE)
		Text(self.screen, f'Lobby duration: {timedelta(seconds=lobby_duration)}', (70, 54), WHITE)

		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (60, self.height-45), 'exit')
		exit_btn.draw()
		chat_btn = ImageButton(self.screen, 'images/game_chat.png', (25, 25), (105, self.height-45), 'info')
		chat_btn.draw()
		next_btn = ImageButton(self.screen, 'images/game_next.png', (25, 25), (150, self.height-45), 'info')
		next_btn.draw()

		return exit_btn, chat_btn, next_btn


	def color_from_player(self):
		colors = {
			0 : 'Green',
			1 : 'Blue',
			2 : 'Yellow',
			3 : 'Red'
		}
		return colors[self.player]


	def send_move(self, pawn_idx):
		run = True
		try:
			game = self.network.send(f'move {self.player} {pawn_idx}')
		except:
			self.draw_error('Could not move pawn.')
			pygame.time.delay(1500)
			pygame.display.update()
			run = False
		return game, run


	def next_player(self):
		run = True
		try:
			game = self.network.send('next_move')
		except:
			self.draw_error('Could not get to next player.')
			pygame.time.delay(1500)
			run = False
		return game, run


	def game_screen(self, game_id):
		pygame.display.set_caption('Ludo Club (Game)')
		run = True
		click = False
		x, y = 50, 50

		try:
			self.player = self.network.send('get_player')
			print('[ > ] You are player:', self.player)
		except:
			self.draw_error('Could not get playerid.')
			pygame.time.delay(2500)
			run = False

		try:
			game = self.network.send(f'username {self.player} {self.user.username} {self.user.id}')
		except:
			self.draw_error('Could not send username.')
			pygame.time.delay(2500)
			run = False

		while run:
			try:
				game = self.network.send(f'get {game_id}')
			except:
				self.draw_error('Could not get game.')
				pygame.time.delay(2500)
				run = False
				break

			if game.player_left():
				self.draw_quitting(game)
				break

			elif not game.connected():
				self.draw_waiting(game)

			elif game.winner is not None:
				self.draw_winner(game)

			else:
				self.screen.fill(BLACK)
				bg = pygame.image.load("images/background.jpg")
				bg = pygame.transform.scale(bg, (self.width, self.height))
				self.screen.blit(bg, (0, 0))

				game_map = pygame.image.load('images/game_map.png')
				game_map = pygame.transform.scale(game_map, (self.width-100, self.height-100))
				self.screen.blit(game_map, (x, y))

				your_pawns = self.draw_pawns(game)
				dice_button = self.draw_dice(game)
				self.draw_players(game)
				exit_btn, chat_btn, next_btn = self.draw_game_screen(game)

				mx, my = pygame.mouse.get_pos()
				if click:
					if game.player_on_move == self.player:
						for pawn_idx, pawn in enumerate(your_pawns):
							if pawn.button.click((mx, my)):
								if game.rolled_dice:
									if pawn.pos < 0:
										if game.dice == 6:
											game, run = self.send_move(pawn_idx)
											self.next_player()
										else:
											pass
									else:
										if pawn.finish:
											if game.dice+pawn.pos > 5:
												pass
											else:
												for _ in range(game.dice):
													game, run = self.send_move(pawn_idx)
												self.next_player()

										else:
											for _ in range(game.dice):
												game, run = self.send_move(pawn_idx)
											self.next_player()
								else:
									pass

						if dice_button.click((mx, my)):
							if not game.rolled_dice:
								for i in range(randint(10, 20)):
									value = randint(1, 6)
									dice_button.image = f'images/cube/cube_{value}.png'
									dice_button.draw()

									pygame.display.update()
									pygame.time.delay(75)

								try:
									game = self.network.send(f'dice {value}')
								except:
									self.draw_error('Could not send dice value.')
									pygame.time.delay(1500)
									run = False
									break

								if game.dice != 6 and game.pawns_free[self.player] == 0:
									self.next_player()
								elif game.pawns_finish[self.player] == 3:
									if game.pawn[self.player][0].finish:
										if game.dice + pawn.pos > 5:
											self.next_player()

								else:
									pass
							else:
								pass

						if next_btn.click((mx, my)):
							if game.rolled_dice:
								self.next_player()
							else:
								pass


					if chat_btn.click((mx, my)):
						self.chat_screen(game_id)

					if exit_btn.click((mx, my)):
						pass


			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game = self.network.send(f'quit')
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						game = self.network.send('quit')
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

			pygame.display.update()
			clock.tick(60)


	def chat_screen(self, game_id):
		pygame.display.set_caption('Ludo Club (Chat)')
		run = True
		click = False

		input_text = InputBox(self.screen, (20, self.height - 45), (self.width - 90, 30), '', RED, WHITE)
		input_send = ImageButton(self.screen, 'images/chat_send.png', (30, 30), (self.width - 45, self.height - 48), 'info')
		exit_btn = ImageButton(self.screen, 'images/main_exit.png', (25, 25), (self.width - 45, 20), 'exit')

		while run:
			try:
				game = self.network.send(f'get {game_id}')
			except:
				self.draw_error('Could not get game.')
				pygame.time.delay(2000)
				run = False
				break

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/background.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			input_text.draw()
			input_send.draw()
			exit_btn.draw()
			Text(self.screen, f'TYPING AS USER: {self.user.username}',(self.width - 65, 32), WHITE, right=True)
			Text(self.screen, f'LUDO CLUB (Chat)',(20, 32), WHITE)

			y = self.height - 60
			for idx, msg in enumerate(game.messages[:30]):
				Text(self.screen, f'# {msg[2]} // {msg[0]} // {msg[1]}', (20, y), WHITE, text_size=20)
				y -= 20

			mx, my = pygame.mouse.get_pos()
			if click:
				if input_send.click((mx, my)):
					try:
						game = self.network.send(f'msg {self.user.username} {input_text.text}')
						input_text.clear()
					except:
						self.draw_error('Could not set message.')
						pygame.time.delay(2000)
						run = False
						break

				if exit_btn.click((mx, my)):
					run = False
					break

			click = False
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game = self.network.send(f'quit')
					self.user.user_quit()
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						click = True

				if event.type == MUSIC_END:
					self.background_music()

				input_text.handle_event(event)
			input_text.update()

			pygame.display.update()
			clock.tick(60)


if __name__ == '__main__':
	app = App(700, 700)
	app.welcome()
