from flask import jsonify, json
import json
import re
import MySQLdb

#Database connection parameters
hostData="us-cdbr-azure-east-c.cloudapp.net"
userData="b24bb34d253579"
passData="850ca65c"
dbData="SafeTicketDB"

def register(jsonArg):
	#JSON Parsing
	correct_data = json.dumps(jsonArg)
	correct = json.loads(correct_data)

	mail = correct["login"]
	password = correct["password"]

	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()

	#Execute proper query
	cur.execute("""INSERT INTO `USERS` (mail, password) VALUES (%s, %s)""", (mail, password,))
	# results=cur.fetchall() #NECESSARY ? ? ?

	return(jsonify(response=200))

def print_msg(jsonMsg):
	print("Came into print method")

	correct_data = json.dumps(jsonMsg)
	print("Correct JSON: " + correct_data)

	correct = json.loads(correct_data)
	print("LOGIN: " + correct["login"])
	print("PASSWORD :" + correct["password"])

	return
