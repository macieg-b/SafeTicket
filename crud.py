from flask import jsonify, json, Response
import MySQLdb

#Database connection parameters
hostData="us-cdbr-azure-east-c.cloudapp.net"
userData="b24bb34d253579"
passData="850ca65c"
dbData="SafeTicketDB"

def register(jsonArg):
	#Database connection, and select object to send queries
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()

	#Parse jsonArg to proper variables
	longitude = arg['x']
	lattitude = arg['y']

	#Execute proper queries
	cur.execute("INSERT INTO cords (id, longitude, latitude) VALUES (6, 11.11, 22.22)")
	return

def print_msg(jsonMsg):
	data = jsonify(jsonMsg)
	login = arg['login']
	password = arg['password']
	print "Email: "+login+" "
	print "Pass: "+password+" "
	return

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

	#Return proper json
	return jsonify(cityname=dbCityName, discount=[dbDiscount], type=[dbType], time=[dbTime])

"""
Function to activate user
- jsonArg has to field 'email' and 'token'
- We have to check if user (identified by email) inserted correct token
  If he did we set active field in Database from 0 to 1
"""
def user_Activate(jsonArg):
	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()
	#Execute proper query
	cur.execute("SELECT `1time_code` FROM `USERS` WHERE Login=%s", [jsonArg['email']])
	results=cur.fetchall()
	#Collect data
	for row in results:
		db1time_code = row[0]

	#Comaprison of 1time_code from json and that one frome Database
	if(jsonArg['token']==db1time_code):
		cur.execute("UPDATE USERS SET Active=1 WHERE Login=%s", [jsonArg['email']])
		retVal=Response(status=200)
	else:
		retVal=Response(status=202)

	#Close Database connection and return response
	cur.close()
	db.close()
	return retVal
