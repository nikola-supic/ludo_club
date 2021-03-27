"""
Created on Wed Mar 10 14:04:30 2021

@author: Sule
@name: user.py
@description: ->
    DOCSTRING:
"""
#!/usr/bin/env python3

from datetime import datetime, timedelta
import mysql.connector

try:
	mydb = mysql.connector.connect(
		host='localhost',
		user='root',
		passwd='',
		database='ludo_club'
		)
	mycursor = mydb.cursor()
	print('[ + ] Successfully connected to database.')
except mysql.connector.errors.InterfaceError: 
	print('[ - ] Can not connect to database.')

def check_login(username, password):
	sql = "SELECT * FROM users WHERE username=%s AND password=%s"
	val = (username, password)

	mycursor.execute(sql, val)
	result = mycursor.fetchone()

	if result is not None:
		return User(result)
	return None

def check_register(username, email, password):
	if len(username) < 4:
		return False
	if len(email) < 4:
		return False
	if len(password) < 8 or len(password) > 24:
		return False

	try:
		time = datetime.now()
		sql = "INSERT INTO users (username, email, password, register_date) VALUES (%s, %s, %s, %s)"
		val = (username, email, password, time, )

		mycursor.execute(sql, val)
		mydb.commit()
		return True
	except:
		pass
	
	return False

def give_win(id):
	sql = "SELECT wins FROM users WHERE id=%s"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	wins = result[0] + 1

	sql = "UPDATE users SET wins=%s WHERE id=%s"
	val = (wins, id, )

	mycursor.execute(sql, val)
	mydb.commit()

def give_defeat(id):
	sql = "SELECT defeats FROM users WHERE id=%s"
	val = (id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	defeats = result[0] + 1

	sql = "UPDATE users SET defeats=%s WHERE id=%s"
	val = (defeats, id, )

	mycursor.execute(sql, val)
	mydb.commit()

def admin_permission(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "UPDATE users SET admin=1 WHERE id=%s"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def ban_player(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "DELETE FROM users WHERE id=%s"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def reset_stats(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "UPDATE users SET wins=0, defeats=0 WHERE id=%s"
	val = (user_id, )

	mycursor.execute(sql, val)
	mydb.commit()

def see_pw(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "SELECT password FROM users WHERE id=%s"
	val = (user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	return result[0]

def last_online(id):
	try:
		user_id = int(id)
	except ValueError:
		return False

	sql = "SELECT last_online FROM users WHERE id=%s"
	val = (user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchone()
	return result[0]

def online_players():
	mycursor.execute("SELECT id, username FROM users WHERE online=1")
	result = mycursor.fetchall()
	return result

def get_winners():
	mycursor.execute("SELECT username, wins FROM users ORDER BY wins DESC")
	result = mycursor.fetchall()
	return result

def get_losers():
	mycursor.execute("SELECT username, defeats FROM users ORDER BY defeats DESC")
	result = mycursor.fetchall()
	return result

class User():
	"""
	DOCSTRING:

	"""
	def __init__(self, result):
		self.id = result[0]
		self.username = result[1]
		self.email = result[2]
		self.password = result[3]
		self.wins = result[4]
		self.defeats = result[5]
		self.register_date = result[6]
		self.last_online = datetime.now() # 7
		self.online = True # 8
		self.admin = result[9]
		self.volume = result[10]

		sql = "UPDATE users SET last_online=%s, online=1 WHERE id=%s"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def user_quit(self):
		self.last_online = datetime.now()
		self.online = False

		sql = "UPDATE users SET last_online=%s, online=0 WHERE id=%s"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_username(self, name):
		if len(name) < 4:
			return False

		self.username = name
		sql = "UPDATE users SET username=%s WHERE id=%s"
		val = (name, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_email(self, email):
		if len(email) < 4:
			return False

		self.email = email
		sql = "UPDATE users SET email=%s WHERE id=%s"
		val = (email, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_password(self, password):
		if len(password) < 8 or len(password) > 24:
			return False

		self.password = password
		sql = "UPDATE users SET password=%s WHERE id=%s"
		val = (password, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def change_volume(self, volume):
		if volume < 0 or volume > 100:
			return False

		self.volume = volume
		sql = "UPDATE users SET volume=%s WHERE id=%s"
		val = (volume, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

