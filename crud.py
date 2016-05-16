from flask import jsonify, json, Response
from random import randint
from  time import gmtime, strftime
from datetime import datetime, timedelta 
import json
import time
import re
import send_email
import MySQLdb

#Database connection parameters
hostData="us-cdbr-azure-east-c.cloudapp.net"
userData="b24bb34d253579"
passData="850ca65c"
dbData="SafeTicketDB"

def register(jsonArg):
	correct_data = json.dumps(json_arg)
	correct_json = json.loads(correct_data)
	
	random_code = randint(100000, 999999)
	mail = correct_json["login"]
	password = correct_json["password"]
	balance = 5.0
	begin_active = "0"
	current_time = datetime.now() + timedelta(minutes=15) + timedelta(hours=2)
	#current_time_plus = current_time.strftime("%Y-%m-%d %H:%M:%S")
	
	db = MySQLdb.connect(host = hostData, user = userData, passwd = passData, db = dbData)
	cur = db.cursor()

	cur.execute("SELECT `Active` FROM `USERS` WHERE `Login` = %s", [correct_json['login']])
	result = cur.fetchall()
	
	query_result = ""
	for row in result:
		query_result = row[0]
	
	switch_result = switch_of_register_call(query_result)

	if (switch_result == "new_code"):
		update_database_code(mail, cur, db)
		response = Response(status = 200)

	if (switch_result == "activated"):
		response = Response(status = 202)

	if (switch_result == "add_new"):
		cur.execute("""INSERT INTO users (Login, Hash_password, Balance, Active, 1time_code, time_exp) VALUES (%s, %s, %s, %s, %s, %s)""", (mail, password, balance, begin_active, random_code, current_time))
		db.commit()

		### Send SMS
		send_email.send(mail, random_code)
		response = Response(status = 200)

	cur.close()
	db.close()

	return(response)

def login(json_arg):
	correct_data = json.dumps(json_arg)
	correct_json = json.loads(correct_data)
	
	mail = correct_json["login"]
	password = correct_json["password"]

	db = MySQLdb.connect(host = hostData, user = userData, passwd = passData, db = dbData)
	cur = db.cursor()

	cur.execute("SELECT `Hash_password` FROM `USERS` WHERE `Login` = %s", (mail))
	result = cur.fetchall()

	query_result = ""
	for row in result:
		query_result = row[0]

	### Correct pass:
	if (password == query_result):
		response = Response(status = 200)

	### User exists, incorrect password
	if (password != query_result and query_result != ""):
		response = Response(status = 401)

	### User does not exists
	if (query_result == ""):
		response = Response(status = 403)

	cur.close()
	db.close()

	return(response)

"""
Function which return information about city
- city is string argument which we use to find proper city in table
- We select information about city from Database and return as json in format:
	{
		"cityname": "Szczecin",
		"discount": ["\"normalne\", \"ulgowe\""	],
		"time": ["\"15min\", \"30min\", \"60min\", \"120min\""],
		"type": ["\"dzienne", \"pospieszne\""		]
	}
"""
def return_CityInfo(city):
	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()
	#Execute proper query
	cur.execute("SELECT `ID`, `CityName`, `Discount`, `Type`, `Time` FROM `CITYINFO` WHERE CityName=%s", [city])
	results=cur.fetchall()

	#Collect data
	for row in results:
		dbCityName = row[1]
		dbDiscount = row[2]
		dbType = row[3]
		dbTime = row[4]
	cur.close()
	db.close()

	#Return proper json - old method
	#return jsonify(cityname=dbCityName, discount=[dbDiscount], type=[dbType], time=[dbTime])

	#Return proper response and json
	data={
		'cityname' : dbCityName,
		'discount' : dbDiscount,
		'type' : dbType,
		'time' : dbTime
	}
	js = json.dumps(data)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

"""
Function to activate user
- jsonArg has two fields 'email' and 'token'
- We have to check if user (identified by email) has inserted correct token
  If he did we set active field in Database from 0 to 1
"""
def user_Activate(jsonArg):
	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()
	#Execute proper query
	cur.execute("SELECT `1time_code` FROM `USERS` WHERE `Login`=%s", [jsonArg['email']])
	results=cur.fetchall()
	#Collect data
	for row in results:
		db1time_code = row[0]

	#Comaprison of 1time_code from json and that one frome Database
	if(jsonArg['token']==db1time_code):
		cur.execute("UPDATE `USERS` SET `Active`=1 WHERE `Login`=%s", [jsonArg['email']])
		retVal=Response(status=200)
	else:
		retVal=Response(status=202)

	#Commit changes, close Database connection and return response
	cur.close()
	db.commit()
	db.close()
	return retVal

def print_msg(jsonMsg):
	print("Came into print method")

	correct_data = json.dumps(jsonMsg)
	print("Correct JSON: " + correct_data)

	correct = json.loads(correct_data)
	print("LOGIN: " + correct["login"])
	print("PASSWORD :" + correct["password"])

	return(jsonify(response=200))


### Additional functions

# 'Python' switch()
def switch_of_register_call(result):
	switcher = {
		"0": "new_code",
		"1": "activated",
	}
	return switcher.get(result, "add_new")

def update_database_code(login, cur, db):
	random_code = randint(100000, 999999)
	cur.execute("UPDATE `USERS` SET `1time_code`=%s WHERE `Login`=%s", (random_code, login))
	db.commit()
	# SEND SMS
	send_email.send(login, random_code)

	return

	

	

