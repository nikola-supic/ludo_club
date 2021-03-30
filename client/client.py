"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: client.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3
#pylint: disable=invalid-name
#pylint: disable=line-too-long

import os
import sys
from _thread import start_new_thread
from datetime import datetime, timedelta
from random import randint
from time import sleep
import pygame

from network import Network
from customs import Text, Button, ImageButton, InputBox
from positions import BOARD_POS, MIDDLE_POS
from positions import GREEN_FINISH, RED_FINISH, BLUE_FINISH, YELLOW_FINISH
from positions import GREEN_START, RED_START, BLUE_START, YELLOW_START
import database as db

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (55, 72, 80)
GREEN = (34, 177, 76)
RED = (237, 28, 36)
BLUE = (15, 39, 99)
YELLOW = (229, 207, 22)

VERSION = 'v0.1'
STARTED = '23.03.2021'
LAST_UPDATE = '27.03.2021'

pygame.font.init()
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

get_level_exp = lambda n: 200 + n * 160 

def name_from_dice(dice):
    name = {
        1 : 'normal',
        2 : 'grey',
        3 : 'special'
    }
    return name[dice]

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
        bg = pygame.image.load("images/error.png")
        bg = pygame.transform.scale(bg, (self.width, self.height))
        self.screen.blit(bg, (0, 0))
        Text(self.screen, f'{msg}', (self.width/2, self.height-60), WHITE, text_size=40, center=True)
        pygame.display.update()


    def welcome(self):
        click = False

        # Login
        x = 40
        y = self.height/2 - 75

        login_name = InputBox(self.screen, (x+25, y+70), (250, 30), 'Sule', RED, GREY)
        login_pass = InputBox(self.screen, (x+25, y+130), (250, 30), '12345678', RED, GREY)
        login_button = Button(self.screen, 'LOGIN', (x+25, y+320), (250, 30), GREY, text_color=WHITE)

        # Register
        x = self.width - 340
        y = self.height/2 - 75

        register_name = InputBox(self.screen, (x+25, y+70), (250, 30), '', RED, GREY)
        register_mail = InputBox(self.screen, (x+25, y+130), (250, 30), '', RED, GREY)
        register_pass = InputBox(self.screen, (x+25, y+190), (250, 30), '', RED, GREY)
        register_button = Button(self.screen, 'REGISTER', (x+25, y+320), (250, 30), GREY, text_color=WHITE)

        while True:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/welcome.png")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            # Login
            x = 40
            y = self.height/2 - 75
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))

            Button(self.screen, 'LOGIN', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            Text(self.screen, 'Enter username:', (x+25, y+60), GREY, text_size=18)
            login_name.draw()
            Text(self.screen, 'Enter password:', (x+25, y+120), GREY, text_size=18)
            login_pass.draw()
            login_button.draw()

            # Register
            x = self.width - 340
            y = self.height/2 - 75
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))

            Button(self.screen, 'REGISTER', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            Text(self.screen, 'Enter username:', (x+25, y+60), GREY, text_size=18)
            register_name.draw()
            Text(self.screen, 'Enter e-mail:', (x+25, y+120), GREY, text_size=18)
            register_mail.draw()
            Text(self.screen, 'Enter password:', (x+25, y+180), GREY, text_size=18)
            register_pass.draw()
            register_button.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
                if login_button.rect.collidepoint((mx, my)):
                    self.user = db.check_login(login_name.text, login_pass.text)

                    x = 40
                    y = self.height/2 - 75
                    if self.user is not None:
                        self.main_menu()
                    else:
                        Text(self.screen, 'WRONG USERNAME OR PASSWORD.', (x+150, y+310), GREY, text_size=20, center=True)
                        login_name.clear()
                        login_pass.clear()

                        pygame.display.update()
                        pygame.time.delay(1500)

                elif register_button.rect.collidepoint((mx, my)):
                    register_name.text.replace(' ', '_')

                    x = self.width - 340
                    y = self.height/2 - 75
                    if db.check_register(register_name.text, register_mail.text, register_pass.text):
                        register_name.clear()
                        register_mail.clear()
                        register_pass.clear()

                        Text(self.screen, 'SUCCESSFULY REGISTERED. NOW LOGIN.', (x+150, y+310), GREY, text_size=20, center=True)
                        pygame.display.update()
                        pygame.time.delay(1500)
                    else:
                        register_name.clear()
                        register_mail.clear()
                        register_pass.clear()

                        Text(self.screen, 'YOU ENTERED SOME WRONG INFO.', (x+150, y+310), GREY, text_size=20, center=True)
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

        button_profile = ImageButton(self.screen, 'images/menu/profile.png', (60, 60),          (20, 20), 'profile')
        button_friends = ImageButton(self.screen, 'images/menu/friends.png', (60, 60),          (100, 20), 'friends')
        button_shop = ImageButton(self.screen, 'images/menu/shop.png', (60, 60),                (180, 20), 'shop')
        button_champions = ImageButton(self.screen, 'images/menu/champions.png', (60, 60),      (260, 20), 'champions')

        button_play = ImageButton(self.screen, 'images/menu/play.png', (120, 120),              (self.width/2-220, self.height/2-60), 'play')
        button_search = ImageButton(self.screen, 'images/menu/search.png', (120, 120),          (self.width/2-60, self.height/2-40), 'search')
        button_computer = ImageButton(self.screen, 'images/menu/computer.png', (120, 120),      (self.width/2+100, self.height/2-60), 'computer')

        button_admin = ImageButton(self.screen, 'images/menu/admin.png', (60, 60),              (self.width-320, self.height-80), 'admin')
        button_settings = ImageButton(self.screen, 'images/menu/settings.png', (60, 60),        (self.width-240, self.height-80), 'settings')
        button_info = ImageButton(self.screen, 'images/menu/info.png', (60, 60),                (self.width-160, self.height-80), 'info')
        button_exit = ImageButton(self.screen, 'images/menu/exit.png', (60, 60),                (self.width-80, self.height-80), 'exit')

        while True:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width-170, -10))

            button_profile.draw()
            button_friends.draw()
            button_shop.draw()
            button_champions.draw()

            button_play.draw()
            button_search.draw()
            button_computer.draw()

            button_admin.draw()
            button_settings.draw()
            button_info.draw()
            button_exit.draw()

            if self.user.exp >= get_level_exp(self.user.level):
                self.level_up()

            mx, my = pygame.mouse.get_pos()
            if click:
                if button_profile.click((mx, my)):
                    self.profile()

                elif button_friends.click((mx, my)):
                    self.friends()

                elif button_shop.click((mx, my)):
                    self.shop()

                elif button_champions.click((mx, my)):
                    self.champions()

                elif button_play.click((mx, my)):
                    self.create_lobby()

                elif button_search.click((mx, my)):
                    self.pick_lobby()

                elif button_computer.click((mx, my)):
                    pass

                elif button_info.click((mx, my)):
                    self.information()

                elif button_settings.click((mx, my)):
                    self.settings()

                elif button_admin.click((mx, my)):
                    if self.user.admin:
                        self.admin_panel()
                    else:
                        self.draw_error('You do not have admin permissions.')
                        pygame.time.delay(1000)

                elif button_exit.click((mx, my)):
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.background_music()

                    if event.key == pygame.K_x:
                        self.user.exp = db.give_exp(self.user.id, 100)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def level_up(self):
        run = True
        click = False

        exp = self.user.exp - get_level_exp(self.user.level)
        if exp < 0:
            exp = 0

        self.user.level = db.give_level(self.user.id, 1)
        self.user.coins = db.give_coins(self.user.id, self.user.level * 100)
        self.user.exp = db.set_exp(self.user.id, exp)

        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/level_up.png")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            Text(self.screen, f'{self.user.level}', (self.width-133, self.height/2+20), WHITE, text_size=84, center=True)
            Text(self.screen, f'{exp} / {get_level_exp(self.user.level)}', (self.width-133, self.height/2+50), WHITE, text_size=22, center=True)
            Text(self.screen, f'+{self.user.level*100} COINS', (self.width-133, self.height/2+95), GREY, text_size=22, center=True)

            Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def profile(self):
        run = True
        click = False

        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            # Game info
            x = self.width/2 - 150
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'PROFILE', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            avatar = pygame.image.load(f"images/avatar/avatar_{self.user.avatar}.png")
            avatar = pygame.transform.scale(avatar, (75, 75))
            self.screen.blit(avatar, (x+20, y+45))

            Text(self.screen, f'Username: {self.user.username}', (x+275, y+50), GREY, text_size=18, right=True)
            Text(self.screen, f'{self.user.email}', (x+275, y+65), GREY, text_size=18, right=True)
            Text(self.screen, f'Level: {self.user.level}', (x+275, y+80), GREY, text_size=18, right=True)
            Text(self.screen, f'Exp: {self.user.exp} / {get_level_exp(self.user.level)}', (x+275, y+95), GREY, text_size=18, right=True)

            dice = pygame.image.load(f"images/dice/{name_from_dice(self.user.dice)}_6.png")
            dice = pygame.transform.scale(dice, (80, 80))
            self.screen.blit(dice, (x+200, y+110))

            Text(self.screen, f'Wins: {self.user.wins}', (x+25, y+135), GREY, text_size=18)
            Text(self.screen, f'Defeats: {self.user.defeats}', (x+25, y+150), GREY, text_size=18)
            Text(self.screen, f'Coins: {self.user.coins}', (x+25, y+165), GREY, text_size=18)
            Text(self.screen, f'Joined: {self.user.register_date}', (x+25, y+180), GREY, text_size=18)

            Text(self.screen, 'GAME BY: SULE', (self.width-20, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def friends(self):
        run = True
        click = False

        # Add friends
        x = 40
        y = self.height/2 - 200
        add_name = InputBox(self.screen, (x+25, y+60), (250, 25), '', RED, GREY)
        add_button = Button(self.screen, 'ADD FRIEND', (x+25, y+130), (250, 25), GREY, text_color=WHITE)

        # Requests
        x = 40
        y = self.height/2

        accept_button = Button(self.screen, 'ACCEPT', (x+25, y+130), (115, 25), GREY, text_color=WHITE)
        decline_button = Button(self.screen, 'DECLINE', (x+160, y+130), (115, 25), GREY, text_color=WHITE)
        request_id = InputBox(self.screen, (x+25, y+100), (250, 25), '', RED, GREY)

        # Friends
        x = self.width - 340
        y = self.height/2 - 200
        delete_id = InputBox(self.screen, (x+25, y+300), (250, 25), '', RED, GREY)
        delete_button = Button(self.screen, 'DELETE FRIEND', (x+25, y+330), (250, 25), GREY, text_color=WHITE)

        # Other
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (40, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            # Add friends
            x = 40
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (300, 180))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'ADD FRIEND', (x+175, y+6), (100, 21), YELLOW, text_color=WHITE).draw()

            Text(self.screen, 'Enter username:', (x+25, y+50), GREY, text_size=16)
            add_name.draw()
            add_button.draw()

            # Requests
            x = 40
            y = self.height/2
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (300, 180))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'REQUESTS', (x+175, y+6), (100, 21), YELLOW, text_color=WHITE).draw()

            result = db.get_requests(self.user.id)
            res_y = y + 40
            for idx, row in enumerate(result[:2]):
                username = db.get_name(row[1])
                if username is not None:
                    Text(self.screen, f'#{idx+1} // ID: {row[0]} // Name: {username}', (x+25, res_y), GREY, text_size=16)
                    res_y += 15

            Text(self.screen, 'Enter request ID:', (x+25, y+90), GREY, text_size=16)
            request_id.draw()
            accept_button.draw()
            decline_button.draw()

            # Friends
            x = self.width - 340
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'FRIENDS', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            result = db.get_friends(self.user.id)
            res_y = y + 50
            for idx, row in enumerate(result):
                if row[0] == self.user.id:
                    username = db.get_name(row[1])
                    status = db.get_online(row[1])
                elif row[1] == self.user.id:
                    username = db.get_name(row[0])
                    status = db.get_online(row[0])

                if username is not None:
                    status = 'ONLINE' if status == 1 else 'OFFLINE'
                    Text(self.screen, f'#{idx+1} // ID: {row[2]} // {username} // {status}', (x+25, res_y), GREY, text_size=16)
                    res_y += 15

            Text(self.screen, 'Enter user ID:', (x+25, y+290), GREY, text_size=16)
            delete_id.draw()
            delete_button.draw()

            # Other
            exit_btn.draw()
            Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-25), GREY, text_size=14, right=True)

            mx, my = pygame.mouse.get_pos()
            if click:
                if add_button.rect.collidepoint((mx, my)):
                    if add_button.text != '':
                        x = 40
                        y = self.height/2 - 200
                        add = db.add_friend(self.user.id, add_name.text)

                        if add:
                            Text(self.screen, 'YOU SUCCESSFULY SEND REQUEST.', (x+150, y+120), GREY, text_size=20, center=True)
                        else:
                            Text(self.screen, 'YOU ENTERED SOME WRONG INFO.', (x+150, y+120), GREY, text_size=20, center=True)

                        add_name.clear()
                        pygame.display.update()
                        pygame.time.delay(1500)

                elif accept_button.rect.collidepoint((mx, my)):
                    if request_id.text != '':
                        x = 40
                        y = self.height/2

                        try:
                            req_id = int(request_id.text)

                            accept = db.accept_friend(req_id)
                            if accept:
                                Text(self.screen, 'YOU SUCCESSFULY ACCEPTED REQUEST.', (x+150, y+75), GREY, text_size=20, center=True)
                            else:
                                Text(self.screen, 'WRONG REQUEST ID.', (x+150, y+75), GREY, text_size=20, center=True)

                            request_id.clear()
                            pygame.display.update()
                            pygame.time.delay(1500)
                        except ValueError:
                            Text(self.screen, 'WRONG REQUEST ID.', (x+150, y+75), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1500)

                elif decline_button.rect.collidepoint((mx, my)):
                    if request_id.text != '':
                        x = 40
                        y = self.height/2

                        try:
                            req_id = int(request_id.text)

                            accept = db.decline_friend(req_id)
                            if accept:
                                Text(self.screen, 'YOU SUCCESSFULY DECLINED REQUEST.', (x+150, y+75), GREY, text_size=20, center=True)
                            else:
                                Text(self.screen, 'WRONG REQUEST ID.', (x+150, y+75), GREY, text_size=20, center=True)

                            request_id.clear()
                            pygame.display.update()
                            pygame.time.delay(1500)
                        except ValueError:
                            Text(self.screen, 'WRONG REQUEST ID.', (x+150, y+75), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1500)

                elif delete_button.rect.collidepoint((mx, my)):
                    if delete_id.text != '':
                        x = self.width - 340
                        y = self.height/2 - 200

                        try:
                            friend_id = int(delete_id.text)
                            delete = db.delete_friend(friend_id)
                            if delete:
                                Text(self.screen, 'YOU SUCCESSFULY DELETED FRIEND.', (x+150, y+275), GREY, text_size=20, center=True)
                            else:
                                Text(self.screen, 'WRONG FRIEND ID.', (x+150, y+275), GREY, text_size=20, center=True)

                            delete_id.clear()
                            pygame.display.update()
                            pygame.time.delay(1500)

                        except ValueError:
                            Text(self.screen, 'WRONG FRIEND ID.', (x+150, y+275), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1500)

                elif exit_btn.click((mx, my)):
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

                add_name.handle_event(event)
                request_id.handle_event(event)
                delete_id.handle_event(event)
            add_name.update()
            request_id.update()
            delete_id.update()

            pygame.display.update()
            clock.tick(60)


    def load_avatar(self, x=0, y=0):
        avatar_list = []
        # row 1
        avatar = ImageButton(self.screen, 'images/avatar/avatar_1.png', (90, 90), (x+40, y+50), '1')
        avatar_list.append(avatar)
        avatar = ImageButton(self.screen, 'images/avatar/avatar_2.png', (90, 90), (x+170, y+50), '2')
        avatar_list.append(avatar)
        # row 2
        avatar = ImageButton(self.screen, 'images/avatar/avatar_3.png', (90, 90), (x+40, y+150), '3')
        avatar_list.append(avatar)
        avatar = ImageButton(self.screen, 'images/avatar/avatar_4.png', (90, 90), (x+170, y+150), '4')
        avatar_list.append(avatar)
        # row 3
        avatar = ImageButton(self.screen, 'images/avatar/avatar_5.png', (90, 90), (x+40, y+250), '5')
        avatar_list.append(avatar)
        avatar = ImageButton(self.screen, 'images/avatar/avatar_6.png', (90, 90), (x+170, y+250), '6')
        avatar_list.append(avatar)

        return avatar_list


    def load_dice(self, x=0, y=0):
        dice_list = []
        # row 1
        dice = ImageButton(self.screen, f'images/dice/normal_{randint(1,6)}.png', (90, 90), (x+40, y+50), '1')
        dice_list.append(dice)
        dice = ImageButton(self.screen, f'images/dice/grey_{randint(1,6)}.png', (90, 90), (x+170, y+50), '2')
        dice_list.append(dice)
        # row 2
        dice = ImageButton(self.screen, f'images/dice/special_{randint(1,6)}.png', (90, 90), (x+40, y+150), '3')
        dice_list.append(dice)

        return dice_list


    def shop(self):
        run = True
        click = False

        # Avatars
        x = 40
        y = 40
        avatar_list = self.load_avatar(x, y)

        # Dice
        x = self.width - 340
        y = 40
        dice_list = self.load_dice(x, y)

        # Powers
        x = 40
        y = self.height - 260

        # Other
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (40, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            # Avatars
            x = 40
            y = 40
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Text(self.screen, '1000 Coins', (x+80, y+18), WHITE, text_size=20)
            Button(self.screen, 'BUY AVATAR', (x+165, y+5), (110, 25), YELLOW, text_color=WHITE).draw()
            for avatar in avatar_list:
                avatar.draw()

            # Dice
            x = self.width - 340
            y = 40
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Text(self.screen, '750 Coins', (x+80, y+18), WHITE, text_size=20)
            Button(self.screen, 'BUY DICE', (x+165, y+5), (110, 25), YELLOW, text_color=WHITE).draw()
            for dice in dice_list:
                dice.draw()

            # Powers
            x = 40
            y = self.height - 260
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (300, 200))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'BUY POWERS', (x+165, y+5), (110, 25), YELLOW, text_color=WHITE).draw()

            # Other
            Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
                for idx, avatar in enumerate(avatar_list):
                    if avatar.click((mx, my)):
                        x = 40
                        y = 40
                        if self.user.coins < 1000:
                            Text(self.screen, 'YOU DO NOT HAVE ENOUGH COINS.', (x+150, y+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                        elif self.user.avatar == idx+1:
                            Text(self.screen, 'YOU ALREADY HAVE THIS AVATAR.', (x+150, y+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                        else:
                            Text(self.screen, 'YOU SUCCESSFULY BOUGHT NEW AVATAR.', (x+150, xy+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                            self.user.coins = db.give_coins(self.user.id, -1000)
                            self.user.avatar = db.set_avatar(self.user.id, idx+1)
                        break

                for idx, dice in enumerate(dice_list):
                    if dice.click((mx, my)):
                        x = self.width - 340
                        y = 40
                        if self.user.coins < 750:
                            Text(self.screen, 'YOU DO NOT HAVE ENOUGH COINS.', (x+150, y+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                        elif self.user.dice == idx+1:
                            Text(self.screen, 'YOU ALREADY HAVE THIS DICE SKIN.', (x+150, y+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                        else:
                            Text(self.screen, 'YOU SUCCESSFULY BOUGHT NEW DICE SKIN.', (x+150, y+360), GREY, text_size=20, center=True)
                            pygame.display.update()
                            pygame.time.delay(1000)

                            self.user.coins = db.give_coins(self.user.id, -750)
                            self.user.dice = db.set_dice(self.user.id, idx+1)
                        break

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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def champions(self):
        run = True
        click = False

        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (40, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            # Winner
            x = 40
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'TOP WINNER', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            result = db.get_winners()
            res_y = y + 50
            for idx, row in enumerate(result):
                Text(self.screen, f'#{idx+1} // {row[0]} // {row[1]}', (x+25, res_y), GREY, text_size=16)
                res_y += 15

            # Loser
            x = self.width - 340
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))
            Button(self.screen, 'TOP LOSERS', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

            result = db.get_losers()
            res_y = y + 50
            for idx, row in enumerate(result):
                Text(self.screen, f'#{idx+1} // {row[0]} // {row[1]}', (x+25, res_y), GREY, text_size=16)
                res_y += 15

            Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def information(self):
        run = True
        click = False
        see_reviews = False

        # Game info
        x = 40
        y = self.height/2 - 200

        rate_us = InputBox(self.screen, (x+25, y+225), (250, 25), '', RED, GREY)
        rate_review = InputBox(self.screen, (x+25, y+270), (250, 25), '', RED, GREY)
        rate_button = Button(self.screen, 'RATE US', (x+25, y+300), (250, 25), GREY, text_color=WHITE)
        review_button = Button(self.screen, 'ALL REVIEWS', (x+25, y+330), (250, 25), GREY, text_color=WHITE)
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            # Game info
            x = 40
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))

            Text(self.screen, 'Game info', (x+80, y+18), WHITE, text_size=20)
            Button(self.screen, f'{VERSION}', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()
            Text(self.screen, 'Game developed by: Sule', (x+25, y+50), GREY, text_size=18)
            Text(self.screen, f'Date started: {STARTED}', (x+25, y+70), GREY, text_size=18)
            Text(self.screen, f'Last update: {LAST_UPDATE}', (x+25, y+90), GREY, text_size=18)

            Text(self.screen, 'Rate us: (1-5)', (x+25, y+215), GREY, text_size=18)
            rate_us.draw()
            Text(self.screen, 'Write review:', (x+25, y+260), GREY, text_size=18)
            rate_review.draw()
            rate_button.draw()
            review_button.draw()

            # Reviews
            if see_reviews:
                x = self.width - 340
                y = self.height/2 - 200

                window = pygame.image.load("images/panel_large.png")
                window = pygame.transform.scale(window, (300, 400))
                self.screen.blit(window, (x, y))

                average = db.get_average()
                Button(self.screen, f'Average: {average[0]:.2f}', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

                result = db.get_reviews()
                res_y = y + 50
                for row in result:
                    Text(self.screen, f'{row[2]} // {row[5]}', (x+25, res_y), GREY, text_size=16)
                    Text(self.screen, f'{row[3]} - {row[4]}', (x+25, res_y+15), GREY, text_size=16)
                    res_y += 30

            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
                if rate_button.rect.collidepoint((mx, my)):
                    if rate_us.text != '':
                        x = 40
                        y = self.height/2 - 200

                        try:
                            value = int(rate_us.text)
                        except ValueError:
                            value = -1

                        if value < 1 or value > 5:
                            self.draw_error('Rate value must be between 1 and 5.')
                            pygame.time.delay(1000)
                        else:
                            add_rating = db.add_rating(self.user.id, self.user.username, value, rate_review.text, self.user.dice)

                            if add_rating:
                                Text(self.screen, 'YOU SUCCESSFULY RATED US.', (x+150, y+230), GREY, text_size=20, center=True)
                                pygame.display.update()
                                pygame.time.delay(1500)
                        rate_review.clear()
                        rate_us.clear()

                elif review_button.rect.collidepoint((mx, my)):
                    if see_reviews:
                        see_reviews = False
                    else:
                        see_reviews = True

                elif exit_btn.click((mx, my)):
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

                rate_us.handle_event(event)
                rate_review.handle_event(event)
            rate_us.update()
            rate_review.update()

            pygame.display.update()
            clock.tick(60)


    def settings(self):
        run = True
        click = False

        # Account info
        x = self.width/2 - 160
        y = 40
        username = InputBox(self.screen, (x+25, y+60), (270, 25), '', RED, GREY)
        email = InputBox(self.screen, (x+25, y+110), (270, 25), '', RED, GREY)
        password = InputBox(self.screen, (x+25, y+157), (270, 25), '', RED, GREY)
        save_acc = Button(self.screen, 'SAVE ACC', (x+195, y+5), (100, 25), YELLOW, text_color=WHITE)

        # Game info
        x = self.width/2 - 160
        y = 260
        volume = InputBox(self.screen, (x+25, y+60), (270, 25), '', RED, GREY)
        save_game = Button(self.screen, 'SAVE GAME', (x+195, y+5), (100, 25), YELLOW, text_color=WHITE)

        # Stats
        x = self.width/2 - 160
        y = 480
        refresh = Button(self.screen, 'REFRESH', (x+195, y+5), (100, 25), YELLOW, text_color=WHITE)

        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width-170, -10))

            # Account info
            x = self.width/2 - 160
            y = 40
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (320, 210))
            self.screen.blit(window, (x, y))

            Text(self.screen, 'Account info', (x+90, y+18), WHITE, text_size=20)
            Text(self.screen, f'Current username: {self.user.username}', (x+25, y+50), GREY, text_size=18)
            username.draw()
            Text(self.screen, f'Current e-mail: {self.user.email}', (x+25, y+100), GREY, text_size=18)
            email.draw()
            Text(self.screen, f'Current password: {self.user.password}', (x+25, y+147), GREY, text_size=18)
            password.draw()
            save_acc.draw()

            # Game info
            x = self.width/2 - 160
            y = 260
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (320, 210))
            self.screen.blit(window, (x, y))

            Text(self.screen, 'Game info', (x+90, y+18), WHITE, text_size=20)
            Text(self.screen, f'Current volume: {self.user.volume}', (x+25, y+50), GREY, text_size=18)
            Text(self.screen, 'Use M to skip song.', (x+25, y+100), GREY, text_size=18)
            volume.draw()
            save_game.draw()

            # Stats
            x = self.width/2 - 160
            y = 480
            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (320, 210))
            self.screen.blit(window, (x, y))

            Text(self.screen, 'Stats', (x+90, y+18), WHITE, text_size=20)
            Text(self.screen, f'Your wins: {self.user.wins}', (x+25, y+50), GREY, text_size=20)
            Text(self.screen, f'Your defeats: {self.user.defeats}', (x+25, y+70), GREY, text_size=20)
            Text(self.screen, f'Register date: {self.user.register_date}', (x+25, y+90), GREY, text_size=20)
            refresh.draw()

            Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
                if save_acc.rect.collidepoint((mx, my)):
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

                elif save_game.rect.collidepoint((mx, my)):
                    if volume.text != '':
                        try:
                            value = int(volume.text)
                        except ValueError:
                            value = -1

                        if value < 0 or value > 100:
                            self.draw_error('Volume value must be between 0 and 100.')
                            pygame.time.delay(1000)
                        else:
                            self.user.change_volume(value)
                            pygame.mixer.music.set_volume(value / 100)
                        volume.clear()

                elif exit_btn.click((mx, my)):
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

                    if event.key == pygame.K_m:
                        self.background_music()

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
        run = True
        click = False
        see_online = False

        x = 40
        y = self.height/2 - 200
        admin_permission = InputBox(self.screen, (x+25, y+60), (250, 25), '', RED, GREY)
        ban_player = InputBox(self.screen, (x+25, y+110), (250, 25), '', RED, GREY)
        reset_stats = InputBox(self.screen, (x+25, y+160), (250, 25), '', RED, GREY)
        see_pw = InputBox(self.screen, (x+25, y+210), (250, 25), '', RED, GREY)
        last_online = InputBox(self.screen, (x+25, y+260), (250, 25), '', RED, GREY)

        online_players = Button(self.screen, 'SEE ONLINE PLAYERS', (x+25, y+330), (250, 25), GREY, text_color=WHITE)
        refresh = Button(self.screen, 'REFRESH', (x+185, y+5), (92, 25), YELLOW, text_color=WHITE)
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (40, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            x = 40
            y = self.height/2 - 200
            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))

            Text(self.screen, 'Admin panel', (x+90, y+18), WHITE, text_size=20)
            Text(self.screen, 'Give admin permissions: (User ID)', (x+25, y+50), GREY, text_size=18)
            admin_permission.draw()
            Text(self.screen, 'Ban user from game: (User ID)', (x+25, y+100), GREY, text_size=18)
            ban_player.draw()
            Text(self.screen, 'Reset wins & defeats: (User ID)', (x+25, y+150), GREY, text_size=18)
            reset_stats.draw()
            Text(self.screen, 'See password: (User ID)', (x+25, y+200), GREY, text_size=18)
            see_pw.draw()
            Text(self.screen, 'Last online: (User ID)', (x+25, y+250), GREY, text_size=18)
            last_online.draw()
            online_players.draw()
            refresh.draw()

            Text(self.screen, 'GAME BY: SULE', (self.width-40, self.height-25), GREY, text_size=14, right=True)
            exit_btn.draw()

            if see_online:
                x = self.width - 340
                y = self.height/2 - 200

                window = pygame.image.load("images/panel_large.png")
                window = pygame.transform.scale(window, (300, 400))
                self.screen.blit(window, (x, y))

                Button(self.screen, 'ONLINE', (x+175, y+5), (100, 25), YELLOW, text_color=WHITE).draw()

                result = db.online_players()
                res_y = y + 50
                for row in result:
                    Text(self.screen, f'#{row[0]} // {row[1]}', (x+25, res_y), GREY, text_size=16)
                    res_y += 15

            mx, my = pygame.mouse.get_pos()
            if click:
                if refresh.rect.collidepoint((mx, my)):
                    if admin_permission.text != '':
                        db.admin_permission(admin_permission.text)

                        admin_permission.clear()
                        pygame.display.update()

                    if ban_player.text != '':
                        db.ban_player(ban_player.text)

                        ban_player.clear()
                        pygame.display.update()

                    if reset_stats.text != '':
                        db.reset_stats(reset_stats.text)

                        reset_stats.clear()
                        pygame.display.update()

                    if see_pw.text != '':
                        user_id = see_pw.text
                        pw = db.see_pw(see_pw.text)
                        see_pw.clear()

                        x = 40
                        y = self.height/2 - 200

                        Text(self.screen, f'User ID: {user_id} // PW: {pw}', (x+25, y+305), GREY, text_size=20)
                        pygame.display.update()
                        pygame.time.delay(2000)

                    if last_online.text != '':
                        user_id = last_online.text
                        online = db.last_online(last_online.text)
                        last_online.clear()

                        x = 40
                        y = self.height/2 - 200

                        Text(self.screen, f'User ID: {user_id} // Last Online: {online}', (x+25, y+320), GREY, text_size=20)
                        pygame.display.update()
                        pygame.time.delay(2000)

                elif online_players.rect.collidepoint((mx, my)):
                    if see_online:
                        see_online = False
                    else:
                        see_online = True

                elif exit_btn.click((mx, my)):
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

                    if event.key == pygame.K_m:
                        self.background_music()

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
        run = True
        click = False

        x = self.width/2 - 150
        y = self.height/2 - 200

        lobby_name = InputBox(self.screen, (x+25, y+70), (250, 30), 'lobby', RED, GREY)
        lobby_pw = InputBox(self.screen, (x+25, y+120), (250, 30), '', RED, GREY)
        lobby_size = InputBox(self.screen, (x+25, y+170), (250, 30), '2', RED, GREY)
        lobby_price = InputBox(self.screen, (x+25, y+220), (250, 30), '100', RED, GREY)

        create = Button(self.screen, 'CREATE', (x+25, y+320), (250, 30), GREY, text_color=WHITE)
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            window = pygame.image.load("images/panel_large.png")
            window = pygame.transform.scale(window, (300, 400))
            self.screen.blit(window, (x, y))

            Button(self.screen, 'CREATE LOBBY', (x+155, y+5), (120, 25), YELLOW, text_color=WHITE).draw()
            Text(self.screen, 'Enter lobby name:', (x+25, y+60), GREY, text_size=18)
            lobby_name.draw()
            Text(self.screen, 'Enter lobby password:', (x+25, y+110), GREY, text_size=18)
            lobby_pw.draw()
            Text(self.screen, 'Enter lobby size:', (x+25, y+160), GREY, text_size=18)
            lobby_size.draw()
            Text(self.screen, 'Enter lobby price:', (x+25, y+210), GREY, text_size=18)
            lobby_price.draw()
            Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)

            create.draw()
            exit_btn.draw()

            mx, my = pygame.mouse.get_pos()
            if click:
                if create.rect.collidepoint((mx, my)):
                    try:
                        size = int(lobby_size.text)
                    except ValueError:
                        size = -1

                    try:
                        price = int(lobby_price.text)
                    except ValueError:
                        price = -1

                    if lobby_name.text == '' or len(lobby_name.text) > 24:
                        self.draw_error('You need to enter valid name for lobby.')
                        pygame.time.delay(1500)

                    elif price < 0:
                        self.draw_error('Price can not be lower then 0.')
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
                            game = self.network.send(f'create {lobby_name.text} {size} {pw} {price}')
                            self.game_screen(game.id)
                        except Exception:
                            self.draw_error('Game error #404.')
                            pygame.time.delay(1500)
                            run = False

                elif exit_btn.click((mx, my)):
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

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

                lobby_name.handle_event(event)
                lobby_size.handle_event(event)
                lobby_pw.handle_event(event)
                lobby_price.handle_event(event)

            lobby_name.update()
            lobby_size.update()
            lobby_pw.update()
            lobby_price.update()

            pygame.display.update()
            clock.tick(60)


    def draw_lobby(self, idx, game):
        row = idx // 2
        col = idx % 2
        x = 90 + col * 270
        y = 50 + row * 160

        join_btn = Button(self.screen, 'JOIN', (x+131, y+100), (105, 28), BLUE, text_color=WHITE)
        join_btn.draw()

        lobby_bg = pygame.image.load("images/panel.png")
        lobby_bg = pygame.transform.scale(lobby_bg, (250, 140))
        self.screen.blit(lobby_bg, (x, y))

        Text(self.screen, f'ID #{idx}', (x+60, y+13), WHITE, text_size=20)
        Text(self.screen, f'NAME: {game.lobby_name}', (x+18, y+40), GREY, text_size=20)
        Text(self.screen, f'JOINED: {game.joined} / {game.lobby_size}', (x+18, y+60), GREY, text_size=20)
        Text(self.screen, f'PRICE: {game.lobby_price}', (x+18, y+80), GREY, text_size=20)

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
        run = True
        click = False

        input_pw = InputBox(self.screen, (90, self.height-50), (250, 30), '', RED, GREY)
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (20, self.height - 45), 'exit')
        while run:
            try:
                waiting = self.network.send('get_lobby')

                if not waiting:
                    self.draw_error('There is no games waiting for player.')
                    pygame.time.delay(2500)
                    run = False
                    break
            except Exception:
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
            Text(self.screen, 'Enter lobby password:', (90, self.height-60), GREY, text_size=18)
            exit_btn.draw()
            Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)

            mx, my = pygame.mouse.get_pos()
            if click:
                if exit_btn.click((mx, my)):
                    run = False

                for idx, game in enumerate(waiting):
                    if join_btn_dict[game.id].rect.collidepoint((mx, my)):
                        if game.lobby_pw == 'None' and game.lobby_price < self.user.coins:
                            game = self.network.send(f'join {game.id}')
                            run = False

                            self.game_screen(game.id)
                        else:
                            if game.lobby_pw == input_pw.text and game.lobby_price < self.user.coins:
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

                    if event.key == pygame.K_m:
                        self.background_music()

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
        x = self.width/2 - 160
        y = self.height/2 - 105

        self.screen.fill(BLACK)
        bg = pygame.image.load("images/background.jpg")
        bg = pygame.transform.scale(bg, (self.width, self.height))
        self.screen.blit(bg, (0, 0))

        logo = pygame.image.load("images/logo.png")
        logo = pygame.transform.scale(logo, (160, 160))
        self.screen.blit(logo, (self.width/2-80, -10))

        window = pygame.image.load("images/panel_small.png")
        window = pygame.transform.scale(window, (320, 210))
        self.screen.blit(window, (x, y))

        Button(self.screen, 'WAITING', (x+195, y+5), (100, 25), YELLOW, text_color=WHITE).draw()
        Text(self.screen, f'WAITING TIME: {timedelta(seconds=duration)}', (x+25, y+50), GREY, text_size=20)
        Text(self.screen, f'JOINED: {game.joined} / {game.lobby_size}', (x+25, y+70), GREY, text_size=20)
        Text(self.screen, f'PASSWORD: {game.lobby_pw}', (x+25, y+90), GREY, text_size=20)
        Text(self.screen, f'PRICE: {game.lobby_price}', (x+25, y+110), GREY, text_size=20)
        Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)

        pygame.display.update()


    def draw_quitting(self, game):
        run = True
        click = False
        duration = int((datetime.now() - game.time_started).total_seconds())
        while run:
            self.screen.fill(BLACK)
            bg = pygame.image.load("images/background.jpg")
            bg = pygame.transform.scale(bg, (self.width, self.height))
            self.screen.blit(bg, (0, 0))

            logo = pygame.image.load("images/logo.png")
            logo = pygame.transform.scale(logo, (160, 160))
            self.screen.blit(logo, (self.width/2-80, -10))

            x = self.width/2 - 190
            y = self.height/2 - 100

            window = pygame.image.load("images/panel_small.png")
            window = pygame.transform.scale(window, (380, 200))
            self.screen.blit(window, (x, y))

            Button(self.screen, 'PLAYER LEFT', (x+255, y+6), (100, 25), YELLOW, text_color=WHITE).draw()
            Text(self.screen, f'GAME TIME: {timedelta(seconds=duration)}', (x+25, y+50), GREY, text_size=20)
            Text(self.screen, f'WINS: {game.wins[self.player]}', (x+25, y+70), GREY, text_size=20)
            Text(self.screen, f'DEFEATS: {game.defeats[self.player]}', (x+25, y+90), GREY, text_size=20)
            Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = self.network.send('quit')
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = self.network.send('quit')
                        run = False

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)


    def draw_winner(self, game_id, time_finished):
        run = True
        click = False
        ready = False

        x = self.width/2 - 190
        y = 75
        ready_btn = Button(self.screen, 'READY', (x+210, y+144), (140, 39), RED, text_size=30, text_color=WHITE)

        try:
            game = self.network.send(f'get {game_id}')
        except Exception:
            self.draw_error('Could not get game.')
            pygame.time.delay(2500)
            run = False

        if self.user.username == game.winner:
            self.user.wins = db.give_win(self.user.id)
            self.user.coins = db.give_coins(self.user.id, ((game.lobby_size-1) * game.lobby_price))
            self.user.exp = db.give_exp(self.user.id, 200)
        else:
            self.user.defeats = db.give_defeat(self.user.id)
            self.user.coins = db.give_coins(self.user.id, -(game.lobby_price))

        while run:
            try:
                game = self.network.send(f'get {game_id}')
            except Exception:
                self.draw_error('Could not get game.')
                pygame.time.delay(2500)
                run = False
                break

            if game.player_left():
                self.draw_quitting(game)
                run = False
                break
            elif game.ready:
                break
            else:
                self.screen.fill(BLACK)
                bg = pygame.image.load("images/game/winner.png")
                bg = pygame.transform.scale(bg, (self.width, self.height))
                self.screen.blit(bg, (0, 0))

                game_duration = int((time_finished - game.time_started).total_seconds())
                lobby_duration = int((datetime.now() - game.lobby_started).total_seconds())

                window = pygame.image.load("images/panel.png")
                window = pygame.transform.scale(window, (380, 200))
                self.screen.blit(window, (x, y))

                Text(self.screen, 'We have a winner!', (x+90, y+19), WHITE, text_size=20)
                Text(self.screen, f'GAME DURATION: {timedelta(seconds=game_duration)}', (x+25, y+50), GREY, text_size=20)
                Text(self.screen, f'LOBBY DURATION: {timedelta(seconds=lobby_duration)}', (x+25, y+70), GREY, text_size=20)
                Text(self.screen, f'WINNER: {game.winner}', (x+25, y+90), GREY, text_size=20)
                Text(self.screen, f'READY: {game.players_ready} / {game.joined}', (x+25, y+110), RED, text_size=20)
                Text(self.screen, 'GAME BY: SULE', (self.width-25, self.height-25), GREY, text_size=14, right=True)
                ready_btn.draw()

                mx, my = pygame.mouse.get_pos()
                if click:
                    if ready_btn.rect.collidepoint((mx, my)):
                        if not ready:
                            try:
                                game = self.network.send('ready')
                                ready = True
                            except Exception:
                                self.draw_error('Could not set you to status ready.')
                                pygame.time.delay(1500)
                                run = False


            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = self.network.send('quit')
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = self.network.send('quit')
                        run = False

                    if event.key == pygame.K_m:
                        self.background_music()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()

            pygame.display.update()
            clock.tick(60)

        return run


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

        img_name = name_from_dice(game.dice_skin)

        dice_button = ImageButton(self.screen, f'images/dice/{img_name}_{game.dice}.png', (40, 40), (self.width/2 - 20, self.height/2 - 20), 'cube')
        dice_button.draw()
        return dice_button

    def draw_players(self, game, start_x, start_y):
        AVATAR_POS = [(181, 181), (368, 368), (181, 368), (368, 181)]


        for idx, user_name in enumerate(game.user_names):
            user_id = game.user_ids[idx]
            avatar = game.user_avatars[idx]
            wins = game.wins[idx]
            defeats = game.defeats[idx]
            finished = game.pawns_finish[idx]

            x, y = AVATAR_POS[idx]
            x += start_x
            y += start_y
            avatar_img = pygame.image.load(f"images/avatar/avatar_{avatar}.png")
            avatar_img = pygame.transform.scale(avatar_img, (50, 50))
            self.screen.blit(avatar_img, (x, y))

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

        Text(self.screen, f'Your color: {self.color_from_player()}', (65, 18), GREY)
        Text(self.screen, f'Game duration: {timedelta(seconds=game_duration)}', (65, 36), GREY)
        Text(self.screen, f'Lobby duration: {timedelta(seconds=lobby_duration)}', (65, 54), GREY)

        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (62, self.height-45), 'exit')
        exit_btn.draw()
        chat_btn = ImageButton(self.screen, 'images/game/chat.png', (25, 25), (105, self.height-45), 'info')
        chat_btn.draw()
        next_btn = ImageButton(self.screen, 'images/game/next.png', (25, 25), (150, self.height-45), 'info')
        next_btn.draw()
        emoji_btn = ImageButton(self.screen, 'images/emoji/normal.png', (25, 25), (195, self.height-45), 'info')
        emoji_btn.draw()

        return exit_btn, chat_btn, next_btn, emoji_btn


    def load_emoji(self, x=0, y=0):
        emoji_list = []
        # row 1
        emoji = ImageButton(self.screen, 'images/emoji/normal.png', (30, 30), (x+30, y+15), 'normal')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/laugh.png', (35, 30), (x+70, y+15), 'laugh')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/bla.png', (30, 30), (x+115, y+15), 'bla')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/boss.png', (30, 30), (x+155, y+15), 'boss')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/kiss.png', (30, 30), (x+195, y+15), 'kiss')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/love.png', (30, 30), (x+235, y+15), 'love')
        emoji_list.append(emoji)

        # row 2
        emoji = ImageButton(self.screen, 'images/emoji/love_2.png', (30, 30), (x+30, y+55), 'love_2')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/angel.png', (30, 30), (x+73, y+55), 'angel')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/eyes.png', (30, 30), (x+115, y+55), 'eyes')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/sad.png', (30, 30), (x+155, y+55), 'sad')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/sad_2.png', (30, 30), (x+195, y+55), 'sad_2')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/hurt.png', (30, 30), (x+235, y+55), 'hurt')
        emoji_list.append(emoji)

        # row 3
        emoji = ImageButton(self.screen, 'images/emoji/omg.png', (30, 30), (x+30, y+95), 'omg')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/omg_2.png', (30, 30), (x+73, y+95), 'omg_2')
        emoji_list.append(emoji)

        emoji = ImageButton(self.screen, 'images/emoji/angry.png', (30, 30), (x+115, y+95), 'angry')
        emoji_list.append(emoji)

        return emoji_list


    def draw_emoji(self):
        x = 140
        y = self.height - 245
        bg = pygame.image.load("images/emoji/window.png")
        bg = pygame.transform.scale(bg, (300, 200))
        self.screen.blit(bg, (x, y))

        emoji_list = self.load_emoji(x, y)
        for emoji in emoji_list:
            emoji.draw()

        return emoji_list


    def draw_sent_emoji(self, player, emoji, start_x, start_y):
        x, y = MIDDLE_POS[player]
        x += start_x
        y += start_y

        emoji_list = self.load_emoji()
        emoji_list[emoji].size = (160, 160)
        emoji_list[emoji].pos = (x-80, y-80)
        emoji_list[emoji].draw()


    def clear_emoji(self):
        sleep(3)

        try:
            game = self.network.send('clear_emoji')
        except Exception:
            self.draw_error('Could not clear emoji.')
            pygame.time.delay(1500)


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

            if game.give_finish_exp:
                self.user.exp = db.give_exp(self.user.id, 100)

                Text(self.screen, f'PAWN FINISHED (+100 EXP)', (self.width/2, 18), GREY, center=True)
                pygame.display.update()
                pygame.time.delay(1000)
        except Exception:
            self.draw_error('Could not move pawn.')
            pygame.time.delay(1500)
            run = False
        return game, run


    def next_player(self):
        run = True
        try:
            game = self.network.send(f'next_move {self.player}')
        except Exception:
            self.draw_error('Could not get to next player.')
            pygame.time.delay(1500)
            run = False
        return game, run


    def check_eat(self, move_idx):
        run = True
        try:
            game = self.network.send(f'check_eat {self.player} {move_idx}')

            if game.give_exp:
                self.user.exp = db.give_exp(self.user.id, 50)

                Text(self.screen, f'PAWN EATEN (+50 EXP)', (self.width/2, 18), GREY, center=True)
                pygame.display.update()
                pygame.time.delay(1000)
        except Exception:
            self.draw_error('Could not check for eating.')
            pygame.time.delay(1500)
            run = False
        return game, run


    def game_screen(self, game_id):
        run = True
        click = False
        x, y = 50, 50
        see_emoji = False
        fix_value = 0

        try:
            self.player = self.network.send('get_player')
            print('[ > ] You are player:', self.player)
        except Exception:
            self.draw_error('Could not get playerid.')
            pygame.time.delay(2500)
            run = False

        try:
            game = self.network.send(f'username {self.player} {self.user.username} {self.user.id} {self.user.avatar}')
        except Exception:
            self.draw_error('Could not send username.')
            pygame.time.delay(2500)
            run = False

        while run:
            try:
                game = self.network.send(f'get {game_id}')
            except Exception:
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
                run = self.draw_winner(game_id, datetime.now())
            else:
                self.screen.fill(BLACK)
                bg = pygame.image.load("images/background.jpg")
                bg = pygame.transform.scale(bg, (self.width, self.height))
                self.screen.blit(bg, (0, 0))

                game_map = pygame.image.load('images/game/map.png')
                game_map = pygame.transform.scale(game_map, (self.width-100, self.height-100))
                self.screen.blit(game_map, (x, y))

                your_pawns = self.draw_pawns(game)
                dice_button = self.draw_dice(game)
                self.draw_players(game, x, y)
                exit_btn, chat_btn, next_btn, emoji_btn = self.draw_game_screen(game)
                if see_emoji:
                    emoji_list = self.draw_emoji()

                if game.emoji is not None:
                    self.draw_sent_emoji(game.emoji_player, game.emoji, x, y)

                mx, my = pygame.mouse.get_pos()
                if click:
                    if see_emoji:
                        for emoji_idx, emoji in enumerate(emoji_list):
                            if emoji.click((mx, my)):
                                try:
                                    game = self.network.send(f'emoji {self.player} {emoji_idx}')
                                except Exception:
                                    self.draw_error('Could not send emoji.')
                                    pygame.time.delay(2500)
                                    run = False
                                    break

                                start_new_thread(self.clear_emoji, ())
                                see_emoji = False

                    else:
                        if game.player_on_move == self.player:
                            for pawn_idx, pawn in enumerate(your_pawns):
                                if pawn.button.click((mx, my)):
                                    if game.rolled_dice:
                                        if pawn.pos < 0:
                                            if game.dice == 6:
                                                game, run = self.send_move(pawn_idx)
                                            else:
                                                pass
                                        else:
                                            if pawn.finish:
                                                if game.dice+pawn.pos > 5:
                                                    pass
                                                else:
                                                    for _ in range(game.dice):
                                                        game, run = self.send_move(pawn_idx)

                                                    if game.dice < 6:
                                                        self.next_player()
                                                    break

                                            else:
                                                for _ in range(game.dice):
                                                    game, run = self.send_move(pawn_idx)

                                                if game.dice < 6:
                                                    self.next_player()
                                                game, run = self.check_eat(pawn_idx)
                                                break
                                    else:
                                        pass

                            if dice_button.click((mx, my)):
                                if not game.rolled_dice:
                                    img = name_from_dice(self.user.dice)

                                    for i in range(randint(10, 20)):
                                        value = randint(1, 6)
                                        dice_button.image = f'images/dice/{img}_{value}.png'
                                        dice_button.draw()

                                        pygame.display.update()
                                        pygame.time.delay(50)

                                    if fix_value != 0:
                                        value = fix_value

                                    self.user.exp = db.give_exp(self.user.id, value)

                                    try:
                                        game = self.network.send(f'dice {value} {self.user.dice}')
                                    except Exception:
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

                            elif next_btn.click((mx, my)):
                                if game.rolled_dice:
                                    self.next_player()
                                else:
                                    pass

                    if chat_btn.click((mx, my)):
                        self.chat_screen(game_id)

                    elif emoji_btn.click((mx, my)):
                        if see_emoji:
                            see_emoji = False
                        else:
                            see_emoji = True

                    elif exit_btn.click((mx, my)):
                        pass


            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = self.network.send('quit')
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game = self.network.send('quit')
                        run = False

                    if event.key == pygame.K_m:
                        self.background_music()

                    if event.key == pygame.K_1:
                        fix_value = 1
                    if event.key == pygame.K_2:
                        fix_value = 2
                    if event.key == pygame.K_3:
                        fix_value = 3
                    if event.key == pygame.K_4:
                        fix_value = 4
                    if event.key == pygame.K_5:
                        fix_value = 5
                    if event.key == pygame.K_6:
                        fix_value = 6

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click = True

                if event.type == MUSIC_END:
                    self.background_music()


            pygame.display.update()
            clock.tick(60)


    def chat_screen(self, game_id):
        run = True
        click = False

        input_text = InputBox(self.screen, (20, self.height - 45), (self.width - 90, 30), '', RED, GREY)
        input_send = ImageButton(self.screen, 'images/game/chat_send.png', (30, 30), (self.width - 45, self.height - 48), 'info')
        exit_btn = ImageButton(self.screen, 'images/exit.png', (25, 25), (self.width - 45, 20), 'exit')

        while run:
            try:
                game = self.network.send(f'get {game_id}')
            except Exception:
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
            Text(self.screen, f'TYPING AS USER: {self.user.username}',(self.width - 65, 32), GREY, right=True)
            Text(self.screen, 'LUDO CLUB (Chat)',(20, 32), GREY)

            y = self.height - 60
            for idx, msg in enumerate(game.messages[:30]):
                Text(self.screen, f'# {msg[2]} // {msg[0]} // {msg[1]}', (20, y), GREY, text_size=20)
                y -= 20

            mx, my = pygame.mouse.get_pos()
            if click:
                if input_send.click((mx, my)):
                    try:
                        game = self.network.send(f'msg {self.user.username} {input_text.text}')
                        input_text.clear()
                    except Exception:
                        self.draw_error('Could not send message.')
                        pygame.time.delay(2000)
                        run = False
                        break

                elif exit_btn.click((mx, my)):
                    run = False
                    break

            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = self.network.send('quit')
                    self.user.user_quit()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                    if event.key == pygame.K_m:
                        self.background_music()

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
