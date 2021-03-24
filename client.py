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
import user

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (15, 39, 99)
RED = (244, 0, 38)
GREEN = (74, 145, 35)
YELLOW = (242, 209, 17)
ORANGE = (242, 118, 9)

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


	def background_music(self):
		songs_list = get_music()
		rand = randint(0, len(songs_list)-1)

		pygame.mixer.music.load('music//' + songs_list[rand])
		pygame.mixer.music.set_volume(self.user.volume / 100)
		pygame.mixer.music.play()


	def welcome(self):
		pygame.display.set_caption('Ludo Club (Welcome)')
		click = False

		# Create left part of screen
		login_name = InputBox(self.screen, (self.width/2-120, self.height - 150), (240, 30), '', BLUE, WHITE)
		login_pass = InputBox(self.screen, (self.width/2-120, self.height - 100), (240, 30), '', BLUE, WHITE)
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

			# Draw left part of screen
			Text(self.screen, 'ENTER USERNAME:', (self.width/2-120, self.height-160), WHITE, text_size=18)
			login_name.draw()
			Text(self.screen, 'ENTER PASSWORD:', (self.width/2-120, self.height-110), WHITE, text_size=18)
			login_pass.draw()
			login_button.draw()

			# Draw right part of screen
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
						Text(self.screen, 'WRONG USERNAME OR PASSWORD.', (self.width - 40, 320), RED, text_size=22, right=True)
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
						
						Text(self.screen, 'SUCCESSFULY REGISTERED, USE THAT INFO TO LOGIN.', (self.width - 40, 320), RED, text_size=22, right=True)
						pygame.display.update()
						pygame.time.delay(1500)
					else:
						register_name.clear()
						register_mail.clear()
						register_pass.clear()
						
						Text(self.screen, 'YOU ENTERED SOME WRONG INFO. TRY AGAIN.', (self.width - 40, 320), RED, text_size=22, right=True)
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

		click = False

		button_settings = ImageButton(self.screen, 'images/main_settings.png', (120, 120), (70, self.height/2 - 70), 'settings')
		button_play = ImageButton(self.screen, 'images/main_start.png', (120, 120), (self.width/2 - 60, self.height/2 - 50), 'start')
		button_admin = ImageButton(self.screen, 'images/main_admin.png', (120, 120), (self.width - 200, self.height/2 - 70), 'exit')
		input_lobby = InputBox(self.screen, (self.width/2 - 100, self.height/2 + 90), (200, 30), '', BLUE, WHITE)

		while True:
			pygame.display.set_caption('Ludo Club (Main Menu)')

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main_bg.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			Text(self.screen, 'LUDO CLUB', (self.width/2, 100), BLUE, text_size=72, center=True)
			Text(self.screen, 'MAIN MENU', (self.width/2, 130), WHITE, text_size=24, center=True)
			Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), WHITE, text_size=14, right=True)

			button_settings.draw()
			Text(self.screen, 'SETTINGS', (70 + 60, self.height/2 + 60), WHITE, text_size=24, center=True)
			button_play.draw()
			Text(self.screen, 'PLAY', (self.width/2, self.height/2 - 60), WHITE, text_size=24, center=True)
			button_admin.draw()
			Text(self.screen, 'ADMIN PANEL', (self.width - 210 + 70, self.height/2 + 60), WHITE, text_size=24, center=True)
			input_lobby.draw()
			Text(self.screen, 'ENTER LOBBY SIZE: (2-4)', (self.width/2, self.height/2 + 80), WHITE, text_size=18, center=True)

			mx, my = pygame.mouse.get_pos()
			if click:
				if button_play.click((mx, my)):
					try:
						lobby_size = int(input_lobby.text)
						input_lobby.clear()

						if lobby_size < 2 or lobby_size > 4:
							Text(self.screen, 'You need to enter number between 2 and 4.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
							pygame.display.update()
							pygame.time.delay(1000)

						else:
							self.start_game(lobby_size)
					except ValueError:
						Text(self.screen, 'You need to enter number between 2 and 4.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
						input_lobby.clear()
						pygame.display.update()
						pygame.time.delay(1000)

				elif button_settings.click((mx, my)):	
					self.settings()

				elif button_admin.click((mx, my)):
					if self.user.admin:
						self.admin_panel()
					else:
						Text(self.screen, 'You do not have admin permissions.', (self.width/2, self.height-40), ORANGE, text_size=24, center=True)
						pygame.display.update()
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

				input_lobby.handle_event(event)
			input_lobby.update()

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
			bg = pygame.image.load("images/main_bg.jpg")
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

			save.draw()

			Text(self.screen, f'Your wins: {self.user.wins}', (self.width/2, self.height-90), WHITE, text_size=18, center=True)
			Text(self.screen, f'Your defeats: {self.user.defeats}', (self.width/2, self.height-75), WHITE, text_size=18, center=True)
			Text(self.screen, f'REGISTRATION DATE: {self.user.register_date}', (self.width/2, self.height-60), WHITE, text_size=18, center=True)

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
							Text(self.screen, 'Volume can not be lower then 0 or bigger then 100.', (self.width/2, self.height-105), BLUE, text_size=24, center=True)
							pygame.display.update()
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
			bg = pygame.image.load("images/main_bg.jpg")
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


	def draw_lobby(self, game):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/lobby.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		duration = int((datetime.now() - game.lobby_started).total_seconds())

		Text(self.screen, 'Waiting for players to join...', (self.width/2, 40), WHITE, text_size=64, center=True)
		Text(self.screen, f'Waiting time: {timedelta(seconds=duration)}', (self.width/2, 70), WHITE, text_size=24, center=True)
		Text(self.screen, f'Players joined: {game.joined} / {game.lobby_size}', (self.width/2, 90), WHITE, text_size=24, center=True)

		pygame.display.update()

	def draw_error(self, msg):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/error.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, 'ERROR', (self.width/2, 25), BLACK, text_size=40, center=True)
		Text(self.screen, f'{msg}', (self.width/2, 60), BLACK, text_size=40, center=True)

		pygame.display.update()

	def draw_winner(self, winner):
		self.screen.fill(BLACK)
		bg = pygame.image.load("images/main/winner.jpg")
		bg = pygame.transform.scale(bg, (self.width, self.height))
		self.screen.blit(bg, (0, 0))
		Text(self.screen, 'WE HAVE A WINNER !', (self.width/2, 25), BLACK, text_size=40, center=True)
		Text(self.screen, f'{winner}', (self.width/2, 60), BLACK, text_size=40, center=True)

		pygame.display.update()

	def start_game(self, lobby_size):
		pass

	def chat_screen(self, n, player):
		pygame.display.set_caption('Ludo Club (Chat)')
		run = True
		click = False

		input_text = InputBox(self.screen, (20, self.height - 45), (self.width - 90, 30), '', GREEN, WHITE)
		input_send = ImageButton(self.screen, 'images/main/send.png', (30, 30), (self.width - 45, self.height - 48), 'info')
		exit_btn = ImageButton(self.screen, 'images/main/exit.png', (25, 25), (self.width - 45, 20), 'exit')

		while run:
			try:
				game = n.send('get')
			except:
				self.draw_error('Could not get game... (player left)')
				pygame.time.delay(2000)
				run = False
				break

			self.screen.fill(BLACK)
			bg = pygame.image.load("images/main/game_bg.jpg")
			bg = pygame.transform.scale(bg, (self.width, self.height))
			self.screen.blit(bg, (0, 0))

			input_text.draw()
			input_send.draw()
			exit_btn.draw()
			Text(self.screen, f'TYPING AS USER: {self.user.username}',(self.width - 65, 32), WHITE, right=True)

			y = self.height - 60
			for idx, msg in enumerate(game.messages[:21]):
				Text(self.screen, f'# {msg[2]} // {msg[0]} // {msg[1]}', (20, y), WHITE, text_size=20)
				y -= 20

			mx, my = pygame.mouse.get_pos()
			if click:
				if input_send.click((mx, my)):
					send_packet = f'msg {self.user.username} {input_text.text}'
					input_text.clear()

					try:
						game = n.send(send_packet)
					except:
						self.draw_error('Could not get game... (after sending message)')
						pygame.time.delay(2000)
						run = False
						break

				if exit_btn.click((mx, my)):
					run = False
					break

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

				input_text.handle_event(event)
			input_text.update()

			pygame.display.update()
			clock.tick(60)


if __name__ == '__main__':
	app = App(700, 700)
	app.welcome()