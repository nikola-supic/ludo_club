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
		host='freedb.tech',
		user='freedbtech_suleludoclub',
		passwd='rootroot',
		database='freedbtech_suleludoclub'
		)
	mycursor = mydb.cursor()
	print('[ + ] Successfully connected to database.')
except mysql.connector.errors.InterfaceError: 
	print('[ - ] Can not connect to database.')

# game related function
def add_rating(user_id, user_name, rating, review):
	try:
		time = datetime.now()
		sql = "INSERT INTO ratings (userid, username, rating, review, time) VALUES (%s, %s, %s, %s, %s)"
		val = (user_id, user_name, rating, review, time, )

		mycursor.execute(sql, val)
		mydb.commit()
		return True
	except Exception as e:
		print(e)
	return False

def get_reviews():
	mycursor.execute("SELECT * FROM ratings WHERE review != ''")
	result = mycursor.fetchall()
	return result

def get_average():
	mycursor.execute("SELECT AVG(rating) AS average FROM ratings")
	result = mycursor.fetchone()
	return result

# friends related functions
def add_friend(user_id, friend_name):
	try:
		sql = "SELECT id FROM users WHERE username=%s LIMIT 1"
		val = (friend_name, )
		mycursor.execute(sql, val)
		result = mycursor.fetchone()
		if result is None:
			return False
		if result[0] == user_id:
			return False

		sql = "INSERT INTO friends (user_id, friend_id, request) VALUES (%s, %s, %s)"
		val = (user_id, result[0], True)
		mycursor.execute(sql, val)
		mydb.commit()
		return True

	except Exception as e:
		print(e)
	return False

def get_requests(user_id):
	sql = "SELECT id, user_id FROM friends WHERE friend_id=%s AND request=1"
	val = (user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchall()
	return result

def accept_friend(req_id):
	try:
		sql = "UPDATE friends SET request=0 WHERE id=%s"
		val = (req_id, ) 

		mycursor.execute(sql, val)
		mydb.commit()
		return True

	except Exception as e:
		print(e)
	return False

def decline_friend(req_id):
	try:
		sql = "DELETE FROM friends WHERE id=%s"
		val = (req_id, ) 

		mycursor.execute(sql, val)
		mydb.commit()
		return True

	except Exception as e:
		print(e)
	return False

def get_friends(user_id):
	sql = "SELECT friend_id, user_id, id FROM friends WHERE (friend_id=%s OR user_id=%s) AND request=0"
	val = (user_id, user_id, )
	mycursor.execute(sql, val)
	result = mycursor.fetchall()
	return result

def delete_friend(id):
	try:
		sql = "DELETE FROM friends WHERE id=%s"
		val = (id, ) 

		mycursor.execute(sql, val)
		mydb.commit()
		return True

	except Exception as e:
		print(e)
	return False

# user related function
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
	except Exception as e:
		print(e)
	return False

def get_name(user_id):
	sql = "SELECT username FROM users WHERE id=%s LIMIT 1"
	val = (user_id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()

	if result is not None:
		return result[0]
	return None

def get_online(user_id):
	sql = "SELECT online FROM users WHERE id=%s LIMIT 1"
	val = (user_id, )

	mycursor.execute(sql, val)
	result = mycursor.fetchone()

	if result is not None:
		return result[0]
	return None

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

def get_top_wins():
	mycursor.execute("SELECT username, wins FROM users ORDER BY wins DESC LIMIT 20")
	result = mycursor.fetchall()
	return result

def get_top_defeats():
	mycursor.execute("SELECT username, defeats FROM users ORDER BY defeats DESC LIMIT 20")
	result = mycursor.fetchall()
	return result

def get_top_coins():
	mycursor.execute("SELECT username, coins FROM users ORDER BY coins DESC LIMIT 20")
	result = mycursor.fetchall()
	return result

def get_top_level():
	mycursor.execute("SELECT username, level FROM users ORDER BY level DESC LIMIT 20")
	result = mycursor.fetchall()
	return result

def get_top_trophies():
	mycursor.execute("SELECT username, trophies FROM users ORDER BY trophies DESC LIMIT 20")
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
		self.coins = result[11]
		self.level = result[12]
		self.exp = result[13]
		self.avatar = result[14]
		self.dice = result[15]
		self.trophies = result[16]
		self.power = result[17]

		sql = "UPDATE users SET last_online=%s, online=1 WHERE id=%s"
		val = (self.last_online, self.id, )

		if self.last_online.day != result[7].day:
			self.coins += 250
			give_coins(self.id, 250)

		mycursor.execute(sql, val)
		mydb.commit()

	def user_quit(self):
		self.last_online = datetime.now()
		self.online = False

		sql = "UPDATE users SET last_online=%s, online=0 WHERE id=%s"
		val = (self.last_online, self.id, )

		mycursor.execute(sql, val)
		mydb.commit()

	def update_sql(self, column, value):
		sql = f"UPDATE users SET {column}=%s WHERE id=%s"
		val = (value, self.id, )
		mycursor.execute(sql, val)
		mydb.commit()

