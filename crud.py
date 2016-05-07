from flask import jsonify, json
import MySQLdb

def add_record(arg):
	data=jsonify(arg)
	longitude=arg['x']
	lattitude=arg['y']
	print "***************\nCoordinates: \n\n"+longitude+"\n"+lattitude+"\n***************"

	db = MySQLdb.connect(host="us-cdbr-azure-east-a.cloudapp.net",
                 	     user="baa57d8d1e6f72",
                	     passwd="4cb8825d",
                             db="YanosikDB")
	cur=db.cursor()
	cur.execute("INSERT INTO cords (id, longitude, latitude) VALUES (6, 11.11, 22.22)")
