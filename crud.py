from flask import jsonify, json, Response
from random import randint
from datetime import datetime, timedelta
from  time import gmtime, strftime
from setting import hostData, userData, passData, dbData
import json
import time
import re
import send_email
import send_sms
import MySQLdb


def pre_register(json_arg):
	correct_data = json.dumps(json_arg)
	correct_json = json.loads(correct_data)

	start_active = "0"
	phone = correct_json["phone"]
	random_code = randint(100000, 999999)
	deadline = datetime.now() + timedelta(minutes=15) + timedelta(hours=2)

	db = MySQLdb.connect(host = hostData, user = userData, passwd = passData, db = dbData)
	cur = db.cursor()

	cur.execute("SELECT `Active`, `time_exp` FROM `USERS` WHERE `phone` = %s", (phone))
	result = cur.fetchall()

	response = Response(status = 200)
	active_result = ""
	exp_time_result = "0"
	current_time = "1"
	for row in result:
		active_result = row[0]
		exp_time_result = row[1]

	if (exp_time_result != "0"):
		dbtime_exp_dateformat = datetime.strptime(exp_time_result, "%Y-%m-%d %H:%M:%S")
		current_time = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") + timedelta(hours = 2)

	switch_result = switch_of_register_call(active_result)

	if (switch_result == "add_new"):
		# send_sms.send_sms(phone, random_code)
		# send_email.send(mail, random_code)

		cur.execute("""INSERT INTO users (Active, 1time_code, time_exp, phone) VALUES (%s, %s, %s, %s)""", (start_active, random_code, deadline, phone))
		db.commit()
		response = Response(status = 200)

	if (switch_result == "new_code" and current_time > dbtime_exp_dateformat):
		# send_sms.send_sms(phone, random_code)
		# send_email.send(mail, random_code)

		cur.execute("UPDATE `USERS` SET `1time_code`=%s, `time_exp`=%s WHERE `phone`=%s", (random_code, deadline, phone))
		db.commit()
		response = Response(status = 200)

	if (switch_result == "new_code" and current_time < dbtime_exp_dateformat):
		data = {}
		data['expiration_time'] = exp_time_result
		correct_json = json.dumps(data)
		response = Response(correct_json, status = 203)


	if (switch_result == "activated"):
		response = Response(status = 202)

	cur.close()
	db.close()

	return(response)

def register(json_arg):
	correct_data = json.dumps(json_arg)
	correct_json = json.loads(correct_data)

	phone = correct_json["phone"]
	mail = correct_json["login"]
	password = correct_json["password"]
	token = correct_json["token"]
	balance = 5.0
	active = "1"

	db = MySQLdb.connect(host = hostData, user = userData, passwd = passData, db = dbData)
	cur = db.cursor()

	cur.execute("SELECT `1time_code`, `time_exp`, `Active` FROM `USERS` WHERE `phone` = %s", (phone))
	result = cur.fetchall()

	if (cur.rowcount == 0):
		cur.close()
		db.close()
		### Set 403 code, what means, something went wrong with database
		return Response(status = 403)
	else:
		for row in result:
			db_1time_code = row[0]
			db_time_exp = row[1]
			db_active = row[2]

		if (db_active == "1"):
			cur.close()
			db.close()

			return(Response(status = 202))

		dbtime_exp_dateformat = datetime.strptime(db_time_exp, "%Y-%m-%d %H:%M:%S")
		current_time = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S") + timedelta(hours = 2)

		if (current_time < dbtime_exp_dateformat):
			if (token == db_1time_code):
				cur.execute("UPDATE `USERS` SET `Login`=%s, `Hash_password`=%s, `Balance`=%s, `Active`=%s WHERE `phone`=%s", (mail, password, balance, active, phone))
				db.commit()
				response = Response(status = 200)

			else:
				response = Response(status = 202)
		else:
			response = Response(status = 203)

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

	response = Response(status = 202)
	query_result = ""
	for row in result:
		query_result = row[0]

	### Correct pass:
	if (password == query_result):
		response = Response(status = 200)

	### User exists, incorrect password
	if (password != query_result and query_result != ""):
		response = Response(status = 202)

	### User does not exist
	if (query_result == ""):
		response = Response(status = 202)

	cur.close()
	db.close()

	return(response)

def return_city_info(city):
	db = MySQLdb.connect(host=hostData, user=userData, passwd=passData, db=dbData)
	cur = db.cursor()

	cur.execute("SELECT COUNT(*) FROM `CITYINFO` WHERE `Cityname`=%s", [city])
	count_result = cur.fetchall()
	count = count_result[0][0]

	if (count == 0):
		### TODO: Set status code
		### Above city does not exist in database
		cur.close()
		db.close()

		return(Response(status = 203))

	cur.execute("SELECT `Discount`, `Type`, `Time`, `Price` FROM `CITYINFO` WHERE `Cityname`=%s", [city])
	result = cur.fetchall()

	cur.close()
	db.close()

	table = []
	json_form = {}

	for i in range(0, count):
		group = {}
		group['discount'] = result[i][0]
		group['type'] = result[i][1]
		group['time'] = result[i][2]
		group['price'] = result[i][3]

		table.append(group)

	json_form['city'] = str(city)
	json_form['cases'] = table

	json_to_send = json.dumps(json_form)
	response = Response(json_to_send, status=200, mimetype='application/json')

	return(response)





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

	return 0
