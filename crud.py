from flask import jsonify, json, Response
from random import randint
from datetime import datetime, timedelta
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
	#Database connection, and select object to send queries
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

	send_emal.send(mail, random_code)

	return(jsonify(response=200))

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

def user_Activate(jsonArg):
	#Database connection
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()
	#Execute proper query
	cur.execute("SELECT `1time_code`, `time_exp` FROM `USERS` WHERE `Login`=%s", [jsonArg['email']])

	results=cur.fetchall()
	if (cur.rowcount==0):
		cur.close()
		db.close()
		return Response(status=202)
	else:
		#Collect data
		for row in results:
			db1time_code = row[0]
			dbtime_exp = row[1]

		#Set proper datatime foramt and add 15 minutes shift
		dbtime_exp_dateformat=datetime.strptime(dbtime_exp, "%Y-%m-%d %H:%M:%S")
		current_time = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") + timedelta(hours=2)
		print current_time
		if (current_time < dbtime_exp_dateformat):
			#Comaprison of 1time_code from json and that one frome Database
			if(jsonArg['token']==db1time_code):
				cur.execute("UPDATE `USERS` SET `Active`=1 WHERE `Login`=%s", [jsonArg['email']])
				retVal=Response(status=200)
			else:
				retVal=Response(status=202)
		else:
			retVal=Response(status=202)

		#Commit changes, close Database connection and return response
		cur.close()
		db.commit()
		db.close()
		return retVal
