from flask import jsonify, json
import MySQLdb

def register(jsonArg):
	#Database connection, and select object to send queries
	db = MySQLdb.connect(host=hostData, user=usetData, passwd=passData, db=dbData)
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
	#Database connection, and select object to send queries
	db = MySQLdb.connect(host=hostData, user=usetData, passwd=passData, db=dbData)
	cur=db.cursor()
	cur.execute("SELECT ")
	return
