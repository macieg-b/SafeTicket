from flask import jsonify, json
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

def return_CityInfo(city):
	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()
	#Send query
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
