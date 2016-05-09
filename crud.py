from flask import jsonify, json
from random import randint
import json
import re
import send_email
import MySQLdb

#Database connection parameters
hostData="us-cdbr-azure-east-c.cloudapp.net"
userData="b24bb34d253579"
passData="850ca65c"
dbData="SafeTicketDB"

def register(jsonArg):
	correct_data = json.dumps(jsonArg)
	correct = json.loads(correct_data)
	random_code = randint(100000, 999999)

	mail = correct["login"]
	password = correct["password"]
	balance = 5.0
	begin_active = 0

	# Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()

	# Execute proper query
	cur.execute("""INSERT INTO users (Login, Hash_password, Balance, Active, 1time_code) VALUES (%s, %s, %s, %s, %s)""", (mail, password, balance, begin_active, random_code))

	db.commit()

	# Close and confirm Database connection
	cur.close()
	db.close()

	return(jsonify(response=200))

def print_msg(jsonMsg):
	print("Came into print method")

	correct_data = json.dumps(jsonMsg)
	print("Correct JSON: " + correct_data)

	correct = json.loads(correct_data)
	print("LOGIN: " + correct["login"])
	print("PASSWORD :" + correct["password"])

	return(jsonify(response=200))

def send(jsonMsg):
	print("Came into method in crud")
	send_email.send("waldeksambor@gmail.com", "444555")

	return(jsonify(response=200))
